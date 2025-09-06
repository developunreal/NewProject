import streamlit as st
import requests
import sounddevice as sd
import scipy.io.wavfile as wav
import pyttsx3

st.title("🎙️ Voice Chatbot with LangChain")

model = st.selectbox("Choose Model", ["llama3.2:latest", "mistral"])
duration = st.slider("Recording duration (sec)", 3, 10, 5)

if st.button("Record"):
    st.write("Recording...")
    fs = 44100
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    wav.write("voice.wav", fs, recording)

    with open("voice.wav", "rb") as f:
        transcript = requests.post("http://localhost:8000/transcribe", files={"file": f}).json()["transcript"]
        st.write(f"🗣️ You said: {transcript}")

        response = requests.post("http://localhost:8000/chat", json={"prompt": transcript}).json()["response"]
        st.write("🤖 Response:")
        st.write(response)

        engine = pyttsx3.init()
        engine.say(response)
        engine.runAndWait()

