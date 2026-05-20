import streamlit as st

st.set_page_config(page_title="Garmin Assistent", page_icon="🎙️")
st.title("🎙️ Garmin Echtzeit-Assistent")

# Holt den gesprochenen Text sicher über die Web-Adresse (URL)
query_params = st.query_params
text = query_params.get("speech", "").lower()

def execute_js(js_code):
    st.components.v1.html(f"<script>{js_code}</script>", height=0, width=0)

# Das veränderte Sprachfeld mit automatischer "Okay Garmin"-Erkennung
html_button = """
<div style="text-align: center; margin-bottom: 20px;">
    <button id="mic-btn" style="background-color: #ff4b4b; color: white; border: none; padding: 12px 24px; font-size: 16px; border-radius: 8px; cursor: pointer; font-weight: bold;">
        🎙️ Sprachsteuerung starten
    </button>
    <p id="status" style="color: #555; font-family: sans-serif; margin-top: 10px;">Bereit. Klicke um zuzuhören.</p>
</div>

<script>
const btn = document.getElementById('mic-btn');
const status = document.getElementById('status');
const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (!Recognition) {
    status.innerText = "Browser blockiert Sprachsteuerung. Nutze Safari (iPad) oder Chrome (PC).";
} else {
    const rec = new Recognition();
    rec.lang = 'de-DE';
    rec.interimResults = false;
    
    btn.addEventListener('click', () => {
        rec.start();
        status.innerText = "🔊 Höre permanent zu... Sage 'Okay Garmin' gefolgt von einem Befehl!";
        btn.style.backgroundColor = "#2baf2b";
    });
    
    rec.onresult = (e) => {
        const resultText = e.results[0][0].transcript;
        const textLower = resultText.toLowerCase();
        
        // Prüft, ob das Aktivierungswort im Satz enthalten ist
        if (textLower.includes("okay garmin") || textLower.includes("ok garmin")) {
            status.innerText = "Aktiviert! Verstanden: " + resultText;
            
            // Text an die URL hängen lädt die Seite mit dem Text neu
            const url = new URL(window.location.href);
            url.searchParams.set("speech", resultText);
            window.parent.location.href = url.toString();
        } else {
            status.innerText = "Ignoriert (Kein 'Okay Garmin' gehört): " + resultText;
            // Hören direkt neu starten, da kein Aktivierungswort dabei war
            setTimeout(() => { rec.start(); }, 400);
        }
    };
    
    rec.onerror = () => { 
        // Startet bei Fehlern/Stille automatisch neu, um aktiv zu bleiben
        setTimeout(() => { rec.start(); }, 400); 
    };
    rec.onend = () => { 
        // Verhindert, dass das Mikrofon einfach ausgeht
        setTimeout(() => { rec.start(); }, 400); 
    };
}
</script>
"""

# Zeigt den Button und die Logik an
st.components.v1.html(html_button, height=100)

# Verarbeitung der Befehle in Python (Nachdem "Okay Garmin" erkannt wurde)
if text:
    st.write(f"**Gehört:** '{text}'")
    antwort = ""

    # Der Piepton wird abgespielt, da "okay garmin" in der URL steckt
    if "okay garmin" in text or "okay gar" in text:
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
