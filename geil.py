import streamlit as st

st.set_page_config(page_title="Garmin Assistent", page_icon="🎙️")
st.title("🎙️ Garmin Echtzeit-Assistent")

# Textfeld als Empfänger für das JavaScript
text = st.text_input("Sprachsteuerung aktiv (Schnittstelle)", key="voice_input").lower()

def execute_js(js_code):
    st.components.v1.html(f"<script>{js_code}</script>", height=0, width=0)

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
            const resultText = e.results[0].transcript; // Fehler korrigiert [0] hinzugefügt
            
            // Sucht das Textfeld auf der Streamlit-Seite und trägt den Text ein
            const inputs = window.parent.document.getElementsByTagName('input');
            if(inputs.length > 0) {
                inputs[0].value = resultText; // Fehler korrigiert [0] hinzugefügt
                inputs[0].dispatchEvent(new Event('input', { bubbles: true }));
                inputs[0].dispatchEvent(new Event('change', { bubbles: true }));
                
                // Simuliert die Enter-Taste, damit Streamlit sofort aufwacht
                inputs[0].form.dispatchEvent(new Event('submit', { bubbles: true }));
            }
        };
    }
    """
    execute_js(js_recognize)

# Verarbeitung der Befehle
if text:
    st.write(f"**Gehört:** '{text}'")
    antwort = ""

    # Wir nutzen "in text", falls du z.B. "okay garmin hallo" sagst
    if "okay garmin" in text:
        js_beep = "const ctx = new AudioContext(); const osc = ctx.createOscillator(); osc.connect(ctx.destination); osc.start(); setTimeout(() => osc.stop(), 300);"
        execute_js(js_beep)
    if "okay gar" in text:
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
