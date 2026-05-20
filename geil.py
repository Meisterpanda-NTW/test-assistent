import streamlit as st

st.set_page_config(page_title="Garmin Assistent", page_icon="🎙️")
st.title("🎙️ Garmin Echtzeit-Assistent")

# Textfeld als Empfänger für das JavaScript
text = st.text_input("Sprachsteuerung aktiv (Schnittstelle)", key="voice_input").lower()

def execute_js(js_code):
    st.components.v1.html(f"<script>{js_code}</script>", height=0, width=0)

# Der magische HTML/JavaScript-Button für Echtzeit-Erkennung im Browser
st.write("Klicke auf 'Zuhören' und sprich direkt los:")
start_button = st.button("🎙️ Zuhören starten")

if start_button:
    js_recognize = """
    const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!Recognition) {
        alert("Dein Browser unterstützt keine Sprachsteuerung. Nutze Safari auf dem iPad oder Chrome auf dem PC.");
    } else {
        const rec = new Recognition();
        rec.lang = 'de-DE';
        rec.interimResults = false;
        rec.maxAlternatives = 1;
        
        rec.start();
        
        rec.onresult = (e) => {
            const resultText = e.results[0][0].transcript;
            // Sucht das Textfeld auf der Streamlit-Seite und trägt den Text blitzschnell ein
            const inputs = window.parent.document.getElementsByTagName('input');
            if(inputs.length > 0) {
                inputs[0].value = resultText;
                inputs[0].dispatchEvent(new Event('input', { bubbles: true }));
                inputs[0].dispatchEvent(new Event('change', { bubbles: true }));
            }
        };
    }
    """
    execute_js(js_recognize)

# Verarbeitung der Befehle
if text:
    st.write(f"**Gehört:** '{text}'")
    antwort = ""

    if "okay garmin" in text:
        js_beep = "const ctx = new AudioContext(); const osc = ctx.createOscillator(); osc.connect(ctx.destination); osc.start(); setTimeout(() => osc.stop(), 300);"
        execute_js(js_beep)

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
        st.empty()
        st.write("### 🛑 Assistent wurde beendet.")

    if antwort:
        js_speech = f"const speech = new SpeechSynthesisUtterance('{antwort}'); speech.lang = 'de-DE'; window.speechSynthesis.speak(speech);"
        execute_js(js_speech)
