import streamlit as st

st.set_page_config(page_title="Garmin Assistent", page_icon="🎙️")
st.title("🎙️ Garmin Echtzeit-Assistent")

# Das versteckte Textfeld, das den Befehl vom JavaScript empfängt
befehl_text = st.text_input("Versteckte Schnittstelle", key="voice_input", label_visibility="collapsed").lower()

def execute_js(js_code):
    st.components.v1.html(f"<script>{js_code}</script>", height=0, width=0)

# Das intelligente 2-Stufen-Sprachsystem im Browser
html_system = """
<div style="text-align: center; margin-bottom: 20px;">
    <button id="mic-btn" style="background-color: #ff4b4b; color: white; border: none; padding: 12px 24px; font-size: 16px; border-radius: 8px; cursor: pointer; font-weight: bold; width: 250px;">
        🎙️ Assistent starten
    </button>
    <p id="status" style="color: #555; font-family: sans-serif; margin-top: 10px; font-weight: bold;">Bereit. Klicke zum Starten.</p>
</div>

<script>
const btn = document.getElementById('mic-btn');
const status = document.getElementById('status');
const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (!Recognition) {
    status.innerText = "Browser blockiert Sprachsteuerung. Bitte Safari (iPad) oder Chrome (PC) nutzen.";
} else {
    const rec = new Recognition();
    rec.lang = 'de-DE';
    rec.interimResults = false;
    
    let warteAufBefehl = false;
    let aktivGeklickt = false;

    function machPiep() {
        const ctx = new AudioContext();
        const osc = ctx.createOscillator();
        osc.connect(ctx.destination);
        osc.start();
        setTimeout(() => osc.stop(), 250);
    }

    btn.addEventListener('click', () => {
        aktivGeklickt = true;
        try { rec.start(); } catch(e) {}
        status.innerText = "💤 Warte auf Aktivierung... (Sage 'Okay Garmin' oder 'Okay Gar')";
        btn.style.backgroundColor = "#ffa500"; 
    });
    
    rec.onresult = (e) => {
        const gehoert = e.results[0][0].transcript.toLowerCase();
        
        // STUFE 1: Wartet auf eines der Aktivierungswörter
        if (!warp = !warteAufBefehl) {
            if (gehoert.includes("okay garmin") || gehoert.includes("ok garmin") || gehoert.includes("okay gar")) {
                machPiep(); 
                warteAufBefehl = true;
                status.innerText = "👂 Ich höre... Sprich jetzt deinen Befehl!";
                btn.style.backgroundColor = "#2baf2b"; 
                rec.stop(); 
            }
        } 
        // STUFE 2: Aktivierung war erfolgreich, trage den Text direkt ins Streamlit-Feld ein
        else {
            status.innerText = "Verstanden: " + gehoert;
            warteAufBefehl = false; 
            
            // Sucht das Streamlit-Textfeld auf der Seite
            const inputs = window.parent.document.getElementsByTagName('input');
            if (inputs.length > 0) {
                inputs[0].value = gehoert;
                inputs[0].dispatchEvent(new Event('input', { bubbles: true }));
                inputs[0].dispatchEvent(new Event('change', { bubbles: true }));
                
                // Simuliert das Absenden (Enter-Taste)
                setTimeout(() => {
                    const form = inputs[0].form;
                    if (form) form.requestSubmit();
                }, 50);
            }
        }
    };
    
    rec.onend = () => {
        if (aktivGeklickt && !status.innerText.includes("Verstanden")) {
            try { rec.start(); } catch(e) {}
        }
    };

    rec.onerror = () => {
        if (aktivGeklickt && !status.innerText.includes("Verstanden")) {
            try { rec.start(); } catch(e) {}
        }
    };
}
</script>
"""

# HTML-Element anzeigen
st.components.v1.html(html_system, height=110)

# Verarbeitung der Befehle in Python
if befehl_text:
    st.write(f"**Verarbeiteter Befehl:** '{befehl_text}'")
    antwort = ""

    if "hallo" in befehl_text:
        antwort = "Hallo wie kann ich dir helfen"
        st.success(antwort)
    elif "fick dich" in befehl_text:
        antwort = "dich auch"
        st.warning(antwort)
    elif "lukas" in befehl_text:
        antwort = "nein nicht lukas"
        st.error(antwort)
    elif "beenden" in befehl_text:
        st.empty()
        st.write("### 🛑 Assistent wurde beendet.")

    if antwort:
        js_speech = f"const speech = new SpeechSynthesisUtterance('{antwort}'); speech.lang = 'de-DE'; window.speechSynthesis.speak(speech);"
        execute_js(js_speech)
