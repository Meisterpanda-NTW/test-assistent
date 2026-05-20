import streamlit as st

st.set_page_config(page_title="Garmin Assistent", page_icon="🎙️")
st.title("🎙️ Garmin Echtzeit-Assistent")

# Holt den finalen Befehl über die URL
query_params = st.query_params
befehl_text = query_params.get("befehl", "").lower()

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
        if (!warteAufBefehl) {
            if (gehoert.includes("okay garmin") || gehoert.includes("ok garmin") || gehoert.includes("okay gar")) {
                machPiep(); 
                warteAufBefehl = true;
                status.innerText = "👂 Ich höre... Sprich jetzt deinen Befehl!";
                btn.style.backgroundColor = "#2baf2b"; 
                
                // Erzwingt das Beenden, damit onend sofort Stufe 2 startet
                rec.stop(); 
            }
        } 
        // STUFE 2: Aktivierung war erfolgreich, verarbeite den echten Befehl
        else {
            status.innerText = "Verarbeite Befehl...";
            warteAufBefehl = false; 
            
            const url = new URL(window.location.href);
            url.searchParams.set("befehl", gehoert);
            window.parent.location.href = url.toString();
        }
    };
    
    // Automatischer Neustart-Schutz
    rec.onend = () => {
        if (aktivGeklickt && !status.innerText.includes("Verarbeite")) {
            try { rec.start(); } catch(e) {}
        }
    };

    rec.onerror = () => {
        if (aktivGeklickt && !status.innerText.includes("Verarbeite")) {
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
