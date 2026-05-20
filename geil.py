import streamlit as st

st.set_page_config(page_title="Garmin Assistent", page_icon="🎙️")
st.title("🎙️ Garmin Echtzeit-Assistent")

# Das intelligente 2-Stufen-Sprachsystem direkt als HTML/JavaScript-Komponente
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
        if (!warteAufBefehl) {
            if (gehoert.includes("okay garmin") || gehoert.includes("ok garmin") || gehoert.includes("okay gar")) {
                machPiep(); 
                warteAufBefehl = true;
                status.innerText = "👂 Ich höre... Sprich jetzt deinen Befehl!";
                btn.style.backgroundColor = "#2baf2b"; 
                rec.stop(); 
            }
        } 
        // STUFE 2: Aktivierung war erfolgreich
        else {
            status.innerText = "Verstanden: " + gehoert;
            warteAufBefehl = false; 
            
            // Der sichere Streamlit-Kanal: Sendet den Text direkt als Event an das Hauptfenster
            window.parent.postMessage({type: 'streamlit:set_component_value', value: gehoert}, '*');
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

# Holt sich den Text über den absolut sicheren Nachrichten-Kanal
# html_element speichert jetzt direkt das Ergebnis aus dem JavaScript!
befehl_text = st.components.v1.html(html_system, height=110)

# Da st.components.v1.html den Rückgabewert nicht direkt anzeigt, 
# nutzen wir einen kleinen Kniff über die Streamlit Session State Steuerung:
if befehl_text and "voice_data" not in st.session_state:
    st.session_state.voice_data = befehl_text

# Verarbeitung der Befehle in Python (Vollkommen ohne Textfeld-Zwang)
if "voice_data" in st.session_state and st.session_state.voice_data:
    text_aktuell = st.session_state.voice_data
    st.write(f"**Verarbeiteter Befehl:** '{text_aktuell}'")
    antwort = ""

    if "hallo" in text_aktuell:
        antwort = "Hallo wie kann ich dir helfen"
        st.success(antwort)
    elif "fick dich" in text_aktuell:
        antwort = "dich auch"
        st.warning(antwort)
    elif "lukas" in text_aktuell:
        antwort = "nein nicht lukas"
        st.error(antwort)
    elif "beenden" in text_aktuell:
        st.session_state.voice_data = ""
        st.empty()
        st.write("### 🛑 Assistent wurde beendet.")

    if antwort:
        # Antwort im Browser laut vorlesen lassen
        js_speech = f"<script>const speech = new SpeechSynthesisUtterance('{antwort}'); speech.lang = 'de-DE'; window.speechSynthesis.speak(speech);</script>"
        st.components.v1.html(js_speech, height=0, width=0)
        
    # Text nach der Verarbeitung leeren, damit er nicht in Endlosschleife spricht
    st.session_state.voice_data = ""
