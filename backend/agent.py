# Purpose: This is the entry-point script for the AI agent. It is responsible for creating and managing the 
# AI Voice Assistant, connecting it to the LiveKit cloud, and defining its core behavior

from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, RoomInputOptions 
# from livekit.agents import BackgroundAudioPlayer, AudioConfig, BuiltinAudioClip
from livekit.plugins import (
    google,
    # cartesia,
    # deepgram,
    noise_cancellation,
    # silero,
)
# from livekit.plugins.turn_detector.multilingual import MultilingualModel
from google.genai import types

from api import Assistant

load_dotenv()

# entrypoint function
async def entrypoint(ctx: agents.JobContext):
    session = AgentSession( # create a session
        llm = google.beta.realtime.RealtimeModel(
            model="gemini-live-2.5-flash-preview",
            voice='Leda',
            # language='hi-IN',  # Removed hardcoded language to allow auto-detection
            # _gemini_tools=[types.GoogleSearch()], #was colliding with other tools so had to remove it.
            temperature=0.2
        ),
    )

    await session.start( # start the session
        room=ctx.room,
        agent=Assistant(),  # Using main assistant with fixed instructions
        room_input_options=RoomInputOptions(
            # LiveKit Cloud enhanced noise cancellation
            # - If self-hosting, omit this parameter
            # - For telephony applications, use `BVCTelephony` for best results
            # noise_cancellation=noise_cancellation.BVCTelephony(), #and for normal voice agent - BVC()
            # noise_cancellation=noise_cancellation.BVCTelephony(),
            noise_cancellation=noise_cancellation.BVC()
        ),
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(
        entrypoint_fnc=entrypoint,
        ))

