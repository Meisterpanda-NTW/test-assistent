import streamlit as st

st.set_page_config(page_title="Garmin Assistent", page_icon="🎙️")
st.title("🎙️ Garmin Echtzeit-Assistent")

# Das hocheffiziente Sprachsystem komplett als ein HTML/JavaScript-Block
html_reine_web_app = """
<div style="text-align: center; margin-bottom: 20px;">
    <button id="mic-btn" style="background-color: #ff4b4b; color: white; border: none; padding: 14px 28px; font-size: 18px; border-radius: 12px; cursor: pointer; font-weight: bold; width: 260px; transition: 0.3s; font-family: sans-serif;">
        🎙️ Befehl einsprechen
    </button>
    <p id="status" style="color: #555; font-family: sans-serif; margin-top: 15px; font-weight: bold; font-size: 15px;">Bereit fürs iPad. Klicke zum Sprechen.</p>
    
    <!-- Hier blenden wir die Antworten direkt auf der Seite ein -->
    <div id="antwort-box" style="margin-top: 20px; padding: 15px; border-radius: 8px; font-family: sans-serif; font-weight: bold; display: none; font-size: 16px;"></div>
</div>

<script>
const btn = document.getElementById('mic-btn');
const status = document.getElementById('status');
const antwortBox = document.getElementById('antwort-box');

// Aktiviert die Spracherkennung (auch für Safari auf iOS/iPad)
const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (!Recognition) {
    status.innerText = "Sprachsteuerung blockiert. Bitte Safari auf dem iPad nutzen!";
} else {
    const rec = new Recognition();
    rec.lang = 'de-DE';
    rec.interimResults = false;
    rec.maxAlternatives = 1;

    // Trickst Safari aus, um die Audio-Ausgabe auf Apple-Geräten vorzubereiten
    let siriStimme = new SpeechSynthesisUtterance("");
    window.speechSynthesis.speak(siriStimme);

    // 1. Funktion für den Aktivierungs-Piepton
    function machPiep() {
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = ctx.createOscillator();
        osc.connect(ctx.destination);
        osc.start();
        setTimeout(() => osc.stop(), 200);
    }

    // 2. FUNKTION: Der Star Wars Imperial March aus Frequenzen
    function spieleStarWars() {
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const melodie = [
            {f: 440.00, d: 0.5},  // A
            {f: 440.00, d: 0.5},  // A
            {f: 440.00, d: 0.5},  // A
            {f: 349.23, d: 0.35}, // F
            {f: 523.25, d: 0.15}, // hohes C
            {f: 440.00, d: 0.5},  // A
            {f: 349.23, d: 0.35}, // F
            {f: 523.25, d: 0.15}, // hohes C
            {f: 440.00, d: 0.6}   // langer Ausklang auf A
        ];

        let startZeit = ctx.currentTime;

        melodie.forEach((note) => {
            const osc = ctx.createOscillator();
            const gainNode = ctx.createGain();
            
            osc.type = 'sawtooth'; // Synthesizer-Sound für Star Wars
            osc.frequency.value = note.f;
            
            gainNode.gain.setValueAtTime(0.3, startZeit);
            gainNode.gain.exponentialRampToValueAtTime(0.01, startZeit + note.d);
            
            osc.connect(gainNode);
            gainNode.connect(ctx.destination);
            
            osc.start(startZeit);
            osc.stop(startZeit + note.d);
            
            startZeit += note.d + 0.05; 
        });
    }

    // 3. Funktion für die Sprachausgabe (Vorlesen)
    function sprich(text) {
        window.speechSynthesis.cancel(); 
        const speech = new SpeechSynthesisUtterance(text);
        speech.lang = 'de-DE';
        
        // >>> HIER STELLST DU DIE TIEFE EIN <<<

        window.speechSynthesis.speak(speech);
    }

    // Klick-Event aktiviert das iPad-Audio und startet das Mikrofon
    btn.addEventListener('click', () => {
        window.speechSynthesis.speak(new SpeechSynthesisUtterance(""));
        
        try { rec.start(); } catch(e) {}
        status.innerText = "🔊 Ich höre zu... Sprich jetzt deinen Befehl!";
        btn.style.backgroundColor = "#2baf2b"; 
        antwortBox.style.display = "none";
    });
    
    rec.onresult = (e) => {
        const gehoert = e.results[0][0].transcript.toLowerCase().trim();
        status.innerText = "Gehört: '" + gehoert + "'";
        
        let antwortText = "";
        let boxFarbe = "#e2e2e2";
        let textFarbe = "#333";

        // Prüft, ob das Aktivierungswort "Okay Garmin" im Satz steckt
        if (gehoert.includes("okay garmin") || gehoert.includes("ok garmin") || gehoert.includes("okay gar")) {
            
            machPiep(); // Macht den Bestätigungs-Piepser
            
            // Deine Befehle direkt in JavaScript geprüft
            if (gehoert.includes("hallo")) {
                antwortText = "Hallo wie kann ich dir helfen";
                boxFarbe = "#d4edda"; // Grün
                textFarbe = "#155724";
            } else if (gehoert.includes("fick dich")) {
                antwortText = "dich auch";
                boxFarbe = "#fff3cd"; // Gelb/Orange
                textFarbe = "#856404";
            } else if (gehoert.includes("lukas")) {
                antwortText = "nein nicht lukas";
                boxFarbe = "#f8d7da"; // Rot
                textFarbe = "#721c24";
            } else if (gehoert.includes("kilyan")) {
                antwortText = "dummer sack";
                boxFarbe = "#fff3cd"; // Gelb/Orange
                textFarbe = "#856404";            
            } else if (gehoert.includes("fick deine mutter")) {
                antwortText = "deine auch";
                boxFarbe = "#fff3cd"; // Gelb/Orange
                textFarbe = "#856404";
            } else if (gehoert.includes("video speichern")) {
                antwortText = "sieg heil";
                boxFarbe = "#fff3cd"; // Gelb/Orange
                textFarbe = "#856404";                      
            } else if (gehoert.includes("f*** deine mutter")) {
                antwortText = "deine auch";
                boxFarbe = "#fff3cd"; // Gelb/Orange
                textFarbe = "#856404";                
            } else if (gehoert.includes("traubenzucker")) {
                antwortText = "schnupf mehr";
                boxFarbe = "#fff3cd"; // Gelb/Orange
                textFarbe = "#856404";    
            } else if (gehoert.includes("sieg heil")) {
                antwortText = "heil hitler";
                boxFarbe = "#fff3cd"; // Gelb/Orange
                textFarbe = "#856404";                   
            } else if (gehoert.includes("schule")) { 
                antwortText = "Hölle gefunden 48°27'22.2 Nord 12°21'35.9 Ost";
                boxFarbe = "#f8d7da"; // Rot
                textFarbe = "#721c24";
            } else if (gehoert.includes("star wars") || gehoert.includes("spiel musik") || gehoert.includes("imperium")) { 
                antwortText = "Möge die Macht mit dir sein.";
                boxFarbe = "#d1ecf1"; // Blau
                textFarbe = "#0c5460";
                spieleStarWars(); // Spielt Darth Vaders Theme ab
            } else if (gehoert.includes("beenden")) {
                antwortText = "programm wird beendet";
                boxFarbe = "#d1ecf1"; // Blau
                textFarbe = "#0c5460";
                rec.stop();
                status.innerText = "🛑 Assistent beendet.";
                btn.style.backgroundColor = "#ff4b4b";
            } else {
                antwortText = "Aktiviert, aber Befehl nicht verstanden.";
                boxFarbe = "#e2e2e2";
            }
            
        } else {
            status.innerText = "Ignoriert (Kein 'Okay Garmin' im Satz): '" + gehoert + "'";
        }

        // Antwort anzeigen und sprechen lassen
        if (antwortText) {
            antwortBox.innerText = antwortText;
            antwortBox.style.backgroundColor = boxFarbe;
            antwortBox.style.color = textFarbe;
            antwortBox.style.display = "block";
            
            // Kleiner Puffer, damit Siri nicht mitten in den Piepton spricht
            setTimeout(() => { sprich(antwortText); }, 250);
        }
        
        btn.style.backgroundColor = "#ff4b4b";
    };
    
    rec.onerror = () => {
        status.innerText = "Bereit fürs iPad. Klicke zum Sprechen.";
        btn.style.backgroundColor = "#ff4b4b";
    };
    rec.onend = () => {
        btn.style.backgroundColor = "#ff4b4b";
    };
}
</script>
"""

# Zeigt die komplette App auf deiner Streamlit-Website an
st.components.v1.html(html_reine_web_app, height=270)
