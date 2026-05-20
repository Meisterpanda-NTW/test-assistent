import streamlit as st

st.set_page_config(page_title="Garmin Assistent", page_icon="🎙️")
st.title("🎙️ Garmin Echtzeit-Assistent")

# Das intelligente 2-Stufen-Sprachsystem als HTML/JavaScript-Komponente
html_system = """
<div style="text-align: center; margin-bottom: 20px;">
    <button id="mic-btn" style="background-color: #ff4b4b; color: white; border: none; padding: 12px 24px; font-size: 16px; border-radius: 8px; cursor: pointer; font-weight: bold; width: 250px; transition: 0.3s;">
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
        
        // STUFE 1: Wartet NUR auf das Aktivierungswort
        if (!warteAufBefehl) {
            if (gehoert.includes("okay garmin") || gehoert.includes("ok garmin") || gehoert.includes("okay gar")) {
                machPiep(); // Macht NUR den Piepton, schickt noch NIX an Python
                warteAufBefehl = true;
                status.innerText = "👂 Ich höre... Sprich jetzt deinen Befehl!";
                btn.style.backgroundColor = "#2baf2b"; 
                rec.stop(); // Stoppt kurz, damit onend sofort Stufe 2 frisch startet
            } else {
                // Falsches Wort -> Direkt weiter auf Garmin warten
                setTimeout(() => { try { rec.start(); } catch(e) {} }, 300);
            }
        } 
        // STUFE 2: Aktivierung war erfolgreich, jetzt wird der echte Befehl an Python geschickt
        else {
            status.innerText = "Übermittle Befehl...";
            warteAufBefehl = false; // Zurücksetzen für das nächste Mal
            
            // Schickt NUR den Befehl über die URL-Parameter an Streamlit
            const url = new URL(window.parent.location.href);
            url.searchParams.set("befehl", gehoert);
            window.parent.location.href = url.toString();
        }
    };
    
    // Hält das Mikrofon im Hintergrund aktiv
    rec.onend = () => {
        if (aktivGeklickt && !status.innerText.includes("Übermittle")) {
            setTimeout(() => { try { rec.start(); } catch(e) {} }, 300);
        }
    };
    rec.onerror = () => {
        if (aktivGeklickt && !status.innerText.includes("Übermittle")) {
            setTimeout(() => { try { rec.start(); } catch(e) {} }, 300);
        }
    };
}
</script>
"""

# Holt den reinen Befehl über die Web-Adresse ab
query_params = st.query_params
text_aktuell = query_params.get("befehl", "").lower()

# Zeigt den großen runden Button an
st.components.v1.html(html_system, height=110)

# Verarbeitung der echten Befehle in Python
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
        # Löscht den Parameter, damit die Seite sauber schließt
        st.query_params.clear()
        st.empty()
        st.write("### 🛑 Assistent wurde beendet.")
        st.info("Du kannst das Browser-Tab jetzt einfach schließen.")

    if antwort:
        # Löscht das Wort aus der Adresszeile nach der Verarbeitung
        st.query_params.clear()
        
        # Antwort im Browser laut vorlesen lassen
        js_speech = f"""
        <script>
        const speech = new SpeechSynthesisUtterance('{antwort}');
        speech.lang = 'de-DE';
        window.speechSynthesis.speak(speech);
        </script>
        """
        st.components.v1.html(js_speech, height=0, width=0)
