# Socratic-AI 🧠🎙️

> **A Real-Time, Voice-First AI Tutor designed for seamless educational interactions.**
> Developed by **Algo Rangers**

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![LiveKit](https://img.shields.io/badge/LiveKit-Powered-FF3366.svg)
![Groq](https://img.shields.io/badge/Groq-Llama_3.3_70b-f4722b.svg)
![AWS](https://img.shields.io/badge/AWS-EC2_Ubuntu-FF9900.svg)

## 📌 Project Overview
Socratic-AI is an intelligent, low-latency conversational AI agent built to act as a personal tutor. By leveraging state-of-the-art Speech-to-Text (STT), Large Language Models (LLMs), and Text-to-Speech (TTS) pipelines, Socratic-AI provides students and professionals with an interactive, voice-first learning experience. 

The architecture is optimized to run efficiently on resource-constrained cloud instances, ensuring maximum uptime and stability during real-time client interactions.

---

## 🏗️ System Architecture
The application follows a modular, real-time pipeline facilitated by LiveKit's WebRTC infrastructure:

1. **Client Interface:** User speaks into the microphone via a web frontend.
2. **WebRTC Transport:** LiveKit securely routes the audio to the backend server.
3. **STT (Speech-to-Text):** OpenAI Whisper transcribes the user's audio into text in real-time.
4. **LLM Engine:** Groq (running `llama-3.3-70b-versatile`) processes the transcription and generates educational, contextual responses.
5. **TTS (Text-to-Speech):** Deepgram synthesizes the LLM's text response back into natural-sounding speech.
6. **Delivery:** The audio stream is sent back to the client instantly.

---

## 🚀 Technology Stack
* **Framework:** Python, LiveKit Agents API
* **Language Model (LLM):** Groq API (`llama-3.3-70b-versatile`)
* **Text-to-Speech (TTS):** Deepgram
* **Speech-to-Text (STT):** OpenAI / Whisper
* **Deployment & Hosting:** AWS EC2 (Ubuntu)

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/Socratic-AI.git
cd Socratic-AI
```

### 2. Set Up Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
Create a `.env` file in the root directory and add your API keys:
```ini
LIVEKIT_URL=your_livekit_websocket_url
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret
GROQ_API_KEY=your_groq_key
DEEPGRAM_API_KEY=your_deepgram_key
OPENAI_API_KEY=your_openai_key
```

---

## 🛡️ Server Optimization (Crucial for EC2)
To prevent `Out of Memory (OOM)` crashes (Exit Code -9) on lightweight AWS EC2 instances, you must configure a Swap file before running the application.

```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

## 🏃‍♂️ Running the Agent

### Development Mode (Interactive)
To run the agent and see real-time logs in your terminal:
```bash
python main.py start
```

### Production Mode (Background Process)
To ensure the AI agent continues running 24/7 even after you close your SSH/EC2 session, use `nohup`:
```bash
nohup python main.py start > agent.log 2>&1 &
```
*To view live logs while it runs in the background:*
```bash
tail -f agent.log
```
*To stop the background process:*
```bash
sudo pkill -f python
```

---

## 🔮 Future Horizons
As Socratic-AI evolves, the following features are planned for future releases:
* **Multimodal Capabilities:** Incorporating screen sharing and visual context analysis so the tutor can "see" the student's work.
* **Emotion & Tone Analysis:** Dynamically adjusting the tutor's pacing and voice tone based on the user's emotional state (frustration, confusion, excitement).
* **Multilingual Expansion:** Expanding beyond English to support diverse regional languages for accessible education.
* **Adaptive Memory Layer:** Implementing persistent session memory so the AI remembers past interactions, struggles, and progress of individual students.

---

*Built with passion by the **Algo Rangers**.*
