import streamlit as st

# Seitentitel im Browser festlegen
st.set_page_config(page_title="Garmin Assistent", page_icon="🎙️")
st.title("🎙️ Garmin Sprachassistent")

# Textfeld für die Spracheingabe (oder manuelle Texteingabe)
text = st.text_input("Was möchtest du sagen?", "").lower()

# Ein unsichtbares JavaScript-Element, um Töne abzuspielen oder zu sprechen
def browser_audio_trigger(js_code):
    st.components.v1.html(f"<script>{js_code}</script>", height=0, width=0)

if text:
    st.write(f"**Gehört:** '{text}'")

    # 1. Aktivierungswort -> Browser piepen lassen
    if "okay garmin" in text:
        # Erzeugt einen Piepton direkt im Browser des Benutzers
        js_beep = "const ctx = new AudioContext(); const osc = ctx.createOscillator(); osc.connect(ctx.destination); osc.start(); setTimeout(() => osc.stop(), 300);"
        browser_audio_trigger(js_beep)

    # 2. Die Befehle prüfen -> Browser sprechen lassen
    antwort = ""
    if "hallo" in text:
        antwort = "Hallo wie kann ich dir helfen"
        st.success(antwort)
        
    elif "fick dich" in text:
        antwort = "dich auch"
        st.warning(antwort)
        
    elif "lukas" in text:
        antwort = "nein nicht lukas"
        st.error(antwort)
        
    elif "beenden" in text:
        antwort = "programm wird beendet"
        st.info("Tab wird geschlossen...")
        
        # JavaScript-Befehl, der versucht das Browser-Tab komplett zuzumachen
        js_close = "window.close();"
        browser_audio_trigger(js_close)


    # Wenn eine Antwort generiert wurde, liest der Browser sie laut vor
    if antwort:
        js_speech = f"const speech = new SpeechSynthesisUtterance('{antwort}'); speech.lang = 'de-DE'; window.speechSynthesis.speak(speech);"
        browser_audio_trigger(js_speech)
