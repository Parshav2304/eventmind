# EventMind – Intelligent Physical Event Concierge

> **Prompt Wars 3 Hackathon Submission**  
> **Vertical:** Physical Event Experience  
> **Built with:** Google Gemini, Flask, Cloud Run

---

## 🌟 Overview

**EventMind** is a state-of-the-art AI assistant designed to solve the "Information Overload" problem at large-scale physical events (conferences, summits, hackathons). Unlike static event apps, EventMind understands the attendee's role, interests, and the real-time context of the venue to provide personalized guidance.

### 🚀 Key Features

- **Context-Aware Recommendations**: Tailors the summit schedule based on user profiles (e.g., "ML Engineer", "Product Lead").
- **Proactive Insights**: Not just "what", but "why" and "how" (e.g., "Arrive 10 mins early for Lab sessions, they fill up fast!").
- **Logistics on Tap**: Instant answers for WiFi, catering locations, parking, and emergency protocols.
- **Dynamic Scheduling**: Helps users navigate between tracks (Generative AI, Agentic Workflows, Data Architecture) without missing key sessions.
- **Micro-interactions**: A premium, mobile-first UI with glassmorphism aesthetics and smooth transitions.

---

## 🏗️ Architecture & Logic

### Intelligent Decision Making
The core of EventMind is a **RAG-lite (Retrieval Augmented Generation with Context Injection)** pattern. 
1. **Context Loading**: On every session start, the entire event knowledge base (sessions, speakers, venue details) is injected into the Gemini 2.0 Flash context window.
2. **User Profiling**: The user's role is persisted allowing the LLM to filter recommendations through a personalized lens.
3. **Reasoning Engine**: Gemini reasons over the conflicting session times to suggest an optimal path that avoids scheduling overlaps while maximizing relevance.

### Google Services Integration
| Service | Implementation |
|---|---|
| **Google Gemini API** | Powers the core reasoning, personalization, and conversational UI. |
| **Google Maps Embed** | Provides interactive venue navigation within the app. |
| **Google Cloud Run** | Scalable, serverless hosting for the Python/Flask backend. |

---

## 🛠️ Tech Stack

- **Backend**: Python 3.12, Flask
- **AI**: Google Generative AI (Gemini 2.0 Flash)
- **Frontend**: Vanilla JS (ES6+), CSS3 (Modern Flex/Grid, Glassmorphism), Lucide Icons
- **Markdown**: Marked.js for rich AI response rendering

---

## 📂 Project Structure

```text
eventmind/
├── app.py               # Flask backend & Gemini reasoning logic
├── index.html           # Premium responsive UI (all-in-one template)
├── requirements.txt     # Dependency list
├── Dockerfile           # Optimized container config for Cloud Run
└── README.md            # Submission documentation
```

---

## ⚡ Quick Start

### 1. Prerequisites
- Python 3.12+
- A Google Gemini API Key

### 2. Local Setup
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/eventmind.git
cd eventmind

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GEMINI_API_KEY="your_api_key_here"

# Run the app
python app.py
```
Access the dashboard at `http://localhost:8080`

---

## 📊 Evaluation Criteria Alignment

- **Code Quality**: Modular logic in `app.py`, clean semantic HTML/CSS in `index.html`.
- **Security**: Environment variable usage for secrets; input sanitization on frontend and backend.
- **Efficiency**: Leveraging `gemini-2.0-flash` for high-speed, low-latency responsiveness.
- **Accessibility**: High contrast ratio, mobile-responsive layout (320px to Desktop), and semantic tags.
- **Google Services**: Deep integration of Gemini for reasoning and Google Maps for logistics.

---

## 📝 Assumptions & Considerations
- The event data is currently pre-loaded in `app.py`. In a production scale-up, this would be fetched from a Firestore or Cloud SQL database.
- Deployment is optimized for Google Cloud Run via the provided `Dockerfile`.

---
*Created by [Your Name] for the Prompt Wars 3 Hackathon.*
