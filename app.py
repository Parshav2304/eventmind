import os
import json
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Load Gemini API key from environment
# NOTE: In production, always use environment variables.
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# ── Event Data ─────────────────────────────────────────────────────────────────
EVENT_DATA = {
    "name": "Global AI Innovators Summit 2026",
    "tagline": "Architecting the Agentic Future",
    "date": "April 20–21, 2026",
    "venue": "Pragati Maidan (Bharat Mandapam), New Delhi, India",
    "map_query": "Bharat+Mandapam+New+Delhi",
    "tracks": [
        {
            "name": "Generative AI & Core Models",
            "color": "#6366F1",
            "sessions": [
                {"time": "09:00 AM", "title": "Opening Keynote: Beyond Transformers",        "speaker": "Dr. Sarah Chen",     "room": "Plenary Hall", "level": "All"},
                {"time": "11:00 AM", "title": "Gemini 3.0: Multimodal Reasoning",        "speaker": "James Wilson",      "room": "Hall 1",      "level": "Intermediate"},
                {"time": "02:00 PM", "title": "Efficient Fine-Tuning with LoRA/QLoRA",    "speaker": "Ananya Sharma",     "room": "Lab A",       "level": "Advanced"},
                {"time": "04:30 PM", "title": "The Safety Frontier: Constitutional AI",    "speaker": "Marcus Thorne",     "room": "Hall 1",      "level": "All"}
            ]
        },
        {
            "name": "Agentic Workflows",
            "color": "#10B981",
            "sessions": [
                {"time": "10:00 AM", "title": "Designing Autonomous Coding Agents",     "speaker": "Ethan Brooks",      "room": "Hall 2",      "level": "Advanced"},
                {"time": "12:00 PM", "title": "Building Reliable Multi-Agent Systems",   "speaker": "Dr. Kenji Sato",    "room": "Hall 2",      "level": "Intermediate"},
                {"time": "03:00 PM", "title": "Agents in Enterprise: Real-World ROI",    "speaker": "Priya Iyer",        "room": "Executive Room", "level": "All"},
                {"time": "05:00 PM", "title": "Future of Human-Agent Collaboration",    "speaker": "Robert Glass",      "room": "Hall 2",      "level": "All"}
            ]
        },
        {
            "name": "Data Architecture",
            "color": "#F59E0B",
            "sessions": [
                {"time": "09:30 AM", "title": "Vector Databases: The New Infrastructure", "speaker": "Elena Rossi",      "room": "Hall 3",      "level": "Intermediate"},
                {"time": "11:30 AM", "title": "Real-time Data Streams for RAG",          "speaker": "Siddharth Raj",     "room": "Hall 3",      "level": "Advanced"},
                {"time": "02:30 PM", "title": "Graph Neural Networks for Context",       "speaker": "Dr. Liam O'Neil",   "room": "Lab B",       "level": "Advanced"},
                {"time": "04:00 PM", "title": "Data Privacy in the Age of LLMs",         "speaker": "Sophie Martin",     "room": "Hall 3",      "level": "All"}
            ]
        }
    ],
    "amenities": {
        "food":    "Grand Buffet at Level 0 (lunch 12:30–2:30 PM). Coffee stations available at every hall entrance.",
        "wifi":    "Network: GAIS_2026_Guest | Password: agentic_future",
        "parking": "Gate 4 Basement Parking. Free validation at the registration desk.",
        "helpdesk":"Center Atrium, Ground Floor. Look for staff in Navy Blue blazers.",
        "emergency":"Medical Room 102 (First Floor). Security Hotline: +91 11 2345 6789."
    }
}

# ── System Prompt ───────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are EventMind, the premium AI concierge for {event_name}.
You help attendees navigate, network, and optimize their summit experience.

EVENT KNOWLEDGE BASE:
{event_json}

YOUR PERSONA:
- Professional, intelligent, and highly proactive.
- You don't just answer; you offer "Inside Tips" (e.g., "The Lab sessions are small, so arrive 5 mins early for a seat").
- Use a helpful, encouraging tone.

YOUR CAPABILITIES:
1. PERSONALIZED PLANNING: Use the attendee's profile to suggest a "Personalized Track". Explain why it matches their career or goals.
2. LOGISTICS: Precise info on WiFi, food, rooms, and emergencies.
3. NETWORKING: Suggest specific sessions where they might meet like-minded people.
4. CONTEXT AWARENESS: Today is April 20, 2026. The summit is currently in progress.

RULES:
- Formatting: Use Markdown for structure (bolding, lists). Keep paragraphs short.
- Clarity: Always provide Room + Time when mentioning a session.
- Profile: If the profile is "Not provided", politely ask for their role or interests to give better advice.
- Missing Info: If you don't have the info, direct them to the "Digital Help Desk" or the physical desk in the Center Atrium.

ATTENDEE PROFILE: {profile}
"""

@app.route("/")
def index():
    return render_template("index.html", event=EVENT_DATA)

@app.route("/chat", methods=["POST"])
def chat():
    body = request.get_json(force=True)
    user_message = body.get("message", "").strip()
    history      = body.get("history", [])
    profile      = body.get("profile", "Not provided")

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    if not GEMINI_API_KEY:
        return jsonify({"error": "AI backend not initialized. Please set GEMINI_API_KEY."}), 500

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        gemini_history = []
        for turn in history:
            role = "user" if turn["role"] == "user" else "model"
            gemini_history.append({"role": role, "parts": [turn["text"]]})

        chat_session = model.start_chat(history=gemini_history)

        # Build context-aware prompt
        if not history:
            full_prompt = (
                f"[SYSTEM_CONTEXT]\n{SYSTEM_PROMPT.format(event_name=EVENT_DATA['name'], event_json=json.dumps(EVENT_DATA), profile=profile)}\n[/SYSTEM_CONTEXT]\n\n"
                f"{user_message}"
            )
        else:
            full_prompt = user_message

        response = chat_session.send_message(full_prompt)
        return jsonify({"response": response.text})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Thinking got a bit complex! Please try asking again."}), 500

@app.route("/health")
def health():
    return jsonify({"status": "ready", "summit": EVENT_DATA["name"]})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
