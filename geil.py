import streamlit as st
from streamlit_mic_recorder import speech_to_text # Das neue Mikrofon-Plugin

st.set_page_config(page_title="Garmin Assistent", page_icon="🎙️")
st.title("🎙️ Garmin Sprachassistent")

# Das JavaScript-Element für Ton und Sprache
def browser_audio_trigger(js_code):
    st.components.v1.html(f"<script>{js_code}</script>", height=0, width=0)

st.write("Klicke auf das Mikrofon und sprich deinen Befehl:")

# Hier ist der neue Mikrofon-Button!
text = speech_to_text(
    language='de',
    start_prompt="🎙️ Aufnahme starten",
    stop_prompt="🛑 Stopp & Senden",
    just_once=True,
    key='audio_in'
)

# Falls etwas gesprochen wurde, verarbeite es
if text:
    text_klein = text.lower()
    st.write(f"**Gehört:** '{text}'")

    # 1. Aktivierungswort
    if "okay garmin" in text_klein:
        js_beep = "const ctx = new AudioContext(); const osc = ctx.createOscillator(); osc.connect(ctx.destination); osc.start(); setTimeout(() => osc.stop(), 300);"
        browser_audio_trigger(js_beep)

    # 2. Befehle prüfen
    antwort = ""
    if "hallo" in text_klein:
        antwort = "Hallo wie kann ich dir helfen"
        st.success(antwort)
        
    elif "fick dich" in text_klein:
        antwort = "dich auch"
        st.warning(antwort)
        
    elif "lukas" in text_klein:
        antwort = "nein nicht lukas"
        st.error(antwort)
        
    elif "beenden" in text_klein:
        antwort = "programm wird beendet"
        st.empty()
        st.write("### 🛑 Assistent wurde beendet.")

    # Wenn eine Antwort da ist, spricht der Browser (iPad/Handy) sie laut aus
    if antwort:
        js_speech = f"const speech = new SpeechSynthesisUtterance('{antwort}'); speech.lang = 'de-DE'; window.speechSynthesis.speak(speech);"
        browser_audio_trigger(js_speech)
