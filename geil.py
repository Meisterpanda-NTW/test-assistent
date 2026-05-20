import streamlit as st

st.set_page_config(page_title="Garmin Assistent", page_icon="🎙️")
st.title("🎙️ Garmin Echtzeit-Assistent")

# Holt den gesprochenen Text absolut sicher aus der Web-Adresse
text_aktuell = st.query_params.get("speech", "").lower()

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
        const gehoert = e.results[0][0].transcript;
        const gehoertLower = gehoert.toLowerCase();
        
        // STUFE 1: Wartet auf eines der Aktivierungswörter
        if (!warteAufBefehl) {
            if (gehoertLower.includes("okay garmin") || gehoertLower.includes("ok garmin") || gehoertLower.includes("okay gar")) {
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
            
            // Sendet den Text über die URL an Streamlit (Lädt die Seite im Hintergrund neu)
            const url = new URL(window.parent.location.href);
            url.searchParams.set("speech", gehoert);
            window.parent.location.href = url.toString();
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

# Verarbeitung der Befehle in Python (Jetzt als echter, reiner Text!)
if text_aktuell:
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
        # Löscht den Text aus der URL beim Beenden
        st.query_params.clear()
        st.empty()
        st.write("### 🛑 Assistent wurde beendet.")
        st.info("Du kannst das Browser-Tab jetzt schließen.")

    if antwort:
        # Löscht den Text aus der URL nach der Verarbeitung, damit er nicht beim Neuladen dauernd spricht
        st.query_params.clear()
        # Antwort im Browser laut vorlesen lassen
        js_speech = f"const speech = new SpeechSynthesisUtterance('{antwort}'); speech.lang = 'de-DE'; window.speechSynthesis.speak(speech);"
        execute_js(js_speech)
