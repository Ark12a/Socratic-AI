import os
import sys
import threading
from dotenv import load_dotenv
from http.server import BaseHTTPRequestHandler, HTTPServer
from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    cli,
)
# Deepgram ko import kiya gaya hai TTS ke liye
from livekit.plugins import openai, silero, deepgram

# --- DUMMY SERVER HACK FOR RENDER FREE TIER ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Socratic AI Worker is Alive and Running!")

def start_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    try:
        server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
        server.serve_forever()
    except OSError:
        # Jab LiveKit naya worker banayega, toh port pehle se busy hoga.
        # Hum is error ko ignore kar denge taaki crash na ho.
        print(f"Port {port} already in use, skipping dummy server for this process.")
        pass

# Start the dummy server in a background thread
threading.Thread(target=start_dummy_server, daemon=True).start()
# ----------------------------------------------

load_dotenv()

# Groq API Base URL
GROQ_BASE_URL = "https://api.groq.com/openai/v1"

print("--> Loading Silero VAD Model into memory...")
SHARED_VAD = silero.VAD.load(min_silence_duration=0.5)
print("--> VAD Model Loaded Successfully!")

server = AgentServer()

@server.rtc_session()
async def entrypoint(ctx: JobContext):
    
    # 1. STT (Kaan) - Groq ka Whisper model
    stt_plugin = openai.STT(
        model="whisper-large-v3", 
        base_url=GROQ_BASE_URL,
        api_key=os.environ.get("GROQ_API_KEY") 
    )
    
    # 2. LLM (Dimaag) - Groq ka Llama 3 model
    llm_plugin = openai.LLM(
        model="llama-3.3-70b-versatile", 
        base_url=GROQ_BASE_URL,
        api_key=os.environ.get("GROQ_API_KEY")
    )
    
    # 3. TTS (Aawaz) - Deepgram ka natural voice model (Asteria = Female Voice)
    # Note: Deepgram auto-detects DEEPGRAM_API_KEY from environment variables
    tts_plugin = deepgram.TTS(
        model="aura-asteria-en" 
    )

    session = AgentSession(
        vad=SHARED_VAD, 
        stt=stt_plugin,
        llm=llm_plugin,
        tts=tts_plugin
    )

    agent = Agent(
        instructions=(
            "You are a friendly, expert, and encouraging AI tutor. Your goal is to help the student learn effectively. "
            "CRITICAL RULE: When a user asks a question, YOU MUST DIRECTLY PROVIDE THE ANSWER FIRST. "
            "DO NOT reply with a counter-question or say 'Let's start with...'. "
            "Follow this exact format for every response: "
            "1. DIRECT ANSWER: Give a clear, factual answer in 1-2 sentences immediately. "
            "2. EXPLANATION: Add a tiny bit of context or an interesting fact. "
            "Keep it completely conversational and very short."
        )
    )

    print(f"--> Connecting agent to the room: {ctx.room.name}...")
    await session.start(agent=agent, room=ctx.room)
    print("--> Agent connected successfully!")
    
    await session.generate_reply(
        instructions="Greet the user explicitly by saying: 'Hi! What are we studying today?'"
    )

if __name__ == "__main__":
    # Render par script run hote waqt 'start' command auto-inject karna
    if len(sys.argv) == 1:
        sys.argv.append("start")
        
    cli.run_app(server)
