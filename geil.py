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

const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (!Recognition) {
    status.innerText = "Sprachsteuerung blockiert. Bitte Safari auf dem iPad nutzen!";
} else {
    const rec = new Recognition();
    rec.lang = 'de-DE';
    rec.interimResults = false;
    rec.maxAlternatives = 1;

    let siriStimme = new SpeechSynthesisUtterance("");
    window.speechSynthesis.speak(siriStimme);

    // Der integrierte Musik-Player für deine hochgeladene MP3
    const audioPlayer = new Audio();

    function machPiep() {
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = ctx.createOscillator();
        osc.connect(ctx.destination);
        osc.start();
        setTimeout(() => osc.stop(), 200);
    }

    function spieleStarWars() {
        audioPlayer.pause(); // Stoppt die echte Musik, falls sie läuft
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const melodie = [
            {f: 440.00, d: 0.5}, {f: 440.00, d: 0.5}, {f: 440.00, d: 0.5},
            {f: 349.23, d: 0.35}, {f: 523.25, d: 0.15}, {f: 440.00, d: 0.5},
            {f: 349.23, d: 0.35}, {f: 523.25, d: 0.15}, {f: 440.00, d: 0.6}
        ];
        let startZeit = ctx.currentTime;
        melodie.forEach((note) => {
            const osc = ctx.createOscillator();
            const gainNode = ctx.createGain();
            osc.type = 'sawtooth';
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

    // SPRIELT DEINE HOCHGELADENE DATEI VOM EIGENEN SERVER AB!
    function spieleEchtesDuelOfFates() {
        window.speechSynthesis.cancel();
        
        // Genialer Trick: Lädt die MP3 direkt aus demselben Ordner deiner Website
        audioPlayer.src = window.location.origin + "/app/static/duel.mp3";
        audioPlayer.volume = 0.5;
        
        audioPlayer.play().catch(e => {
            // Falls Streamlit die Datei in einem anderen Pfad versteckt, hier der sichere Ersatz-Pfad
            audioPlayer.src = "duel.mp3";
            audioPlayer.play().catch(err => {
                status.innerText = "Fehler beim Laden deiner 'duel.mp3' auf GitHub.";
            });
        });
    }

    function sprich(text) {
        window.speechSynthesis.cancel(); 
        const speech = new SpeechSynthesisUtterance(text);
        speech.lang = 'de-DE';
        window.speechSynthesis.speak(speech);
    }

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

        if (gehoert.includes("okay garmin") || gehoert.includes("ok garmin") || gehoert.includes("okay gar")) {
            
            machPiep(); 
            
            if (gehoert.includes("hallo")) {
                antwortText = "Hallo wie kann ich dir helfen";
                boxFarbe = "#d4edda";
            } else if (gehoert.includes("fick dich")) {
                antwortText = "dich auch";
                boxFarbe = "#fff3cd";
            } else if (gehoert.includes("lukas")) {
                antwortText = "nein nicht lukas";
                boxFarbe = "#f8d7da";
            } else if (gehoert.includes("kilyan")) {
                antwortText = "dummer sack";
                boxFarbe = "#fff3cd";
            } else if (gehoert.includes("fick deine mutter")) {
                antwortText = "deine auch";
                boxFarbe = "#fff3cd";
            } else if (gehoert.includes("video speichern")) {
                antwortText = "sieg heil";
                boxFarbe = "#fff3cd";
            } else if (gehoert.includes("f*** deine mutter")) {
                antwortText = "deine auch";
                boxFarbe = "#fff3cd";
            } else if (gehoert.includes("traubenzucker")) {
                antwortText = "schnupf mehr";
                boxFarbe = "#fff3cd";
            } else if (gehoert.includes("sieg heil")) {
                antwortText = "heil hitler";
                boxFarbe = "#fff3cd";
            } else if (gehoert.includes("schule")) { 
                antwortText = "Hölle gefunden 48°27'22.2 Nord 12°21'35.9 Ost";
                boxFarbe = "#f8d7da";
            } else if (gehoert.includes("star wars") || gehoert.includes("spiel musik") || gehoert.includes("imperium")) { 
                antwortText = "Möge die Macht mit dir sein.";
                boxFarbe = "#d1ecf1";
                spieleStarWars();
            } else if (gehoert.includes("duel of fates") || gehoert.includes("schicksal") || gehoert.includes("kampf")) { 
                antwortText = "Spiele dein hochgeladenes Duel of the Fates Thema.";
                boxFarbe = "#f8d7da";
                textFarbe = "#721c24";
                spieleEchtesDuelOfFates(); // Startet das Lied von deiner eigenen Seite
            } else if (gehoert.includes("beenden") || gehoert.includes("stopp")) {
                antwortText = "Musik gestoppt, programm wird beendet";
                boxFarbe = "#d1ecf1";
                audioPlayer.pause(); // Schaltet deine Musik sofort aus
                rec.stop();
                status.innerText = "🛑 Assistent beendet.";
            } else {
                antwortText = "Aktiviert, aber Befehl nicht verstanden.";
                boxFarbe = "#e2e2e2";
            }
            
        } else {
            status.innerText = "Ignoriert (Kein 'Okay Garmin' im Satz): '" + gehoert + "'";
        }

        if (antwortText) {
            antwortBox.innerText = antwortText;
            antwortBox.style.backgroundColor = boxFarbe;
            antwortBox.style.color = textFarbe;
            antwortBox.style.display = "block";
            if (!gehoert.includes("duel of fates") && !gehoert.includes("schicksal") && !gehoert.includes("kampf")) {
                setTimeout(() => { sprich(antwortText); }, 250);
            }
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

# Zeigt die App auf deiner Streamlit-Website an
st.components.v1.html(html_reine_web_app, height=270)
