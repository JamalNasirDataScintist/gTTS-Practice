# ================== IMPORT LIBRARIES ==================
import streamlit as st
import datetime
import wikipedia
import urllib.parse
from gtts import gTTS
from io import BytesIO

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="Browser Virtual Assistant",
    page_icon="🤖",
    layout="centered"
)

# ================== TEXT TO SPEECH ==================
def talk(text):
    tts = gTTS(text=text, lang="en")
    audio_bytes = BytesIO()
    tts.write_to_fp(audio_bytes)
    st.audio(audio_bytes.getvalue(), format="audio/mp3")

# ================== ASSISTANT LOGIC ==================
def run_assistant(command):

    # PLAY SONG ON YOUTUBE
    if command.startswith("play"):
        song = command.replace("play", "").strip()
        query = urllib.parse.quote(song)
        url = f"https://www.youtube.com/results?search_query={query}"
        response = f"Playing {song} on YouTube"
        talk(response)
        st.link_button("▶ Play on YouTube", url)
        return response

    # CURRENT TIME
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        response = f"The current time is {current_time}"
        talk(response)
        return response

    # WIKIPEDIA SEARCH
    elif command.startswith("search"):
        topic = command.replace("search", "").strip()
        try:
            info = wikipedia.summary(topic, sentences=2)
            talk(info)
            return info
        except wikipedia.exceptions.DisambiguationError:
            response = "Please be more specific in your search"
            talk(response)
            return response
        except wikipedia.exceptions.PageError:
            response = "No information found"
            talk(response)
            return response

    # OPEN YOUTUBE
    elif "open youtube" in command:
        url = "https://www.youtube.com"
        response = "Opening YouTube"
        talk(response)
        st.link_button("📺 Open YouTube", url)
        return response

    # WHO ARE YOU
    elif "who are you" in command:
        response = "I am a browser based virtual assistant created by Jamal"
        talk(response)
        return response

    # DEFAULT
    else:
        response = "Sorry, I do not understand that command"
        talk(response)
        return response

# ================== STREAMLIT UI ==================
st.title("🤖 Browser-Based Virtual Assistant")
st.write("Type a command and click **Run Assistant**")

command = st.text_input(
    "💬 Enter your command",
    placeholder="e.g. play despacito, search python, open youtube, what is the time"
)

if st.button("🚀 Run Assistant"):
    if command.strip():
        st.success(f"🗣 You said: {command}")
        reply = run_assistant(command.lower())
        st.info(reply)
    else:
        st.warning("Please enter a command")
