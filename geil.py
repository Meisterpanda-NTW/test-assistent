import streamlit as st
import base64
import os

st.set_page_config(page_title="Garmin Assistent", page_icon="🎙️")
st.title("🎙️ Garmin Echtzeit-Assistent")

# Funktion: Wir wandeln die Musikdateien in unblockierbare Daten-Streams um
def get_audio_base64(dateiname):
    if os.path.exists(dateiname):
        with open(dateiname, "rb") as f:
            data = f.read()
            return base64.b64encode(data).decode()
    return ""

# Hier werden beide Lieder vom Server geladen und vorbereitet
duel_base64 = get_audio_base64("duel.mp3")
cantina_base64 = get_audio_base64("cantina.mp3")
hello_base64 = get_audio_base64("hello.mp3") 
clone_base64 = get_audio_base64("clone.mp3") 

# Der HTML/JavaScript-Block als normaler Text OHNE f-String (Klammerfehler ab jetzt UNMÖGLICH!)
html_reine_web_app = """
<div style="text-align: center; margin-bottom: 20px;">
    <button id="mic-btn" style="background-color: #ff4b4b; color: white; border: none; padding: 14px 28px; font-size: 18px; border-radius: 12px; cursor: pointer; font-weight: bold; width: 260px; transition: 0.3s; font-family: sans-serif;">
        🎙️ Befehl einsprechen
    </button>
    <p id="status" style="color: #555; font-family: sans-serif; margin-top: 15px; font-weight: bold; font-size: 15px;">Klicke zum Sprechen.</p>
    
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

    // Der integrierte Musik-Player
    const audioPlayer = new Audio();

    function machPiep() {
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = ctx.createOscillator();
        osc.connect(ctx.destination);
        osc.start();
        setTimeout(() => { osc.stop(); }, 200);
    }

    function spieleStarWars() {
        audioPlayer.pause(); 
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

    // LIED 1: Duel of the Fates (Ganz normale, einfache JavaScript-Klammern!)
    function spieleEchtesDuelOfFates() {
        window.speechSynthesis.cancel();
        const base64Data = "PLATZHALTER_DUEL_MUSIC";
        if (base64Data.length > 0) {
            audioPlayer.src = "data:audio/mp3;base64," + base64Data;
            audioPlayer.volume = 0.5;
            audioPlayer.play().catch(e => {});
        } else {
            status.innerText = "Fehler: 'duel.mp3' fehlt auf dem Server.";
        }
    }

    // LIED 2: Cantina Band Song (Ganz normale, einfache JavaScript-Klammern!)
    function spieleCantinaSong() {
        window.speechSynthesis.cancel();
        const base64Data = "PLATZHALTER_CANTINA_MUSIC";
        if (base64Data.length > 0) {
            audioPlayer.src = "data:audio/mp3;base64," + base64Data;
            audioPlayer.volume = 0.5;
            audioPlayer.play().catch(e => {});
        } else {
            status.innerText = "Fehler: 'cantina.mp3' fehlt auf dem Server.";
        }
    }
    // LIED 2: Cantina Band Song (Ganz normale, einfache JavaScript-Klammern!)
    function spieleHello() {
        window.speechSynthesis.cancel();
        const base64Data = "PLATZHALTER_Hello_MUSIC";
        if (base64Data.length > 0) {
            audioPlayer.src = "data:audio/mp3;base64," + base64Data;
            audioPlayer.volume = 0.5;
            audioPlayer.play().catch(e => {});
        } else {
            status.innerText = "Fehler: 'hello.mp3' fehlt auf dem Server.";
        }
    }
       // LIED 2: Cantina Band Song (Ganz normale, einfache JavaScript-Klammern!)
    function spieleCLONESong() {
        window.speechSynthesis.cancel();
        const base64Data = "PLATZHALTER_CLONE_MUSIC";
        if (base64Data.length > 0) {
            audioPlayer.src = "data:audio/mp3;base64," + base64Data;
            audioPlayer.volume = 0.5;
            audioPlayer.play().catch(e => {});
        } else {
            status.innerText = "Fehler: 'CLONE.mp3' fehlt auf dem Server.";
        }
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
            
            // Deine komplette originale Befehlsliste
            if (gehoert.includes("hallo")) {
                antwortText = "";
                boxFarbe = "#d4edda";
                spieleHello();
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
            } else if (gehoert.includes("befehle")) {
                antwortText = "Befehle lauten: Hallo, video speichern, traubenzucker, schule, starwars, episode 1, episode 4, beenden";
                boxFarbe = "#fff3cd";                
            } else if (gehoert.includes("sieg heil")) {
                antwortText = "heil hitler";
                boxFarbe = "#fff3cd";
            } else if (gehoert.includes("schule")) { 
                antwortText = "Hölle gefunden 48°27'22.2 Nord 12°21'35.9 Ost";
                boxFarbe = "#f8d7da";
            } else if (gehoert.includes("imperium")) { 
                antwortText = "Möge die Macht mit dir sein.";
                boxFarbe = "#d1ecf1";
                spieleStarWars();
            } else if (gehoert.includes("duel of fates") || gehoert.includes("schicksal") || gehoert.includes("episode 1")) { 
                antwortText = "starte Episode 1";
                boxFarbe = "#f8d7da";
                textFarbe = "#721c24";
                spieleEchtesDuelOfFates(); 
            } else if (gehoert.includes("clone wars")) { 
                antwortText = "Begunn";
                boxFarbe = "#d1ecf1";
                spieleCloneMusic();    
            } else if (gehoert.includes("cantina") || gehoert.includes("song") || gehoert.includes("episode 4")) { 
                antwortText = "starte Episode 4";
                boxFarbe = "#fff3cd";
                textFarbe = "#856404";
                spieleCantinaSong(); 
            } else if (gehoert.includes("beenden") || gehoert.includes("stopp")) {
                antwortText = "Musik gestoppt, programm wird beendet";
                boxFarbe = "#d1ecf1";
                audioPlayer.pause(); 
                rec.stop();
                status.innerText = "🛑 Assistent beendet.";
            } else {
                antwortText = "Aktiviert, aber Befehl nicht verstanden.";
                boxFarbe = "#e2e2e2";
            }
            
        } else {
            status.innerText = "Ignoriert (Kein 'Okay Garmin'): '" + gehoert + "'";
        }

        if (antwortText) {
            antwortBox.innerText = antwortText;
            antwortBox.style.backgroundColor = boxFarbe;
            antwortBox.style.color = textFarbe;
            antwortBox.style.display = "block";
            if (!gehoert.includes("duel of fates") && !gehoert.includes("schicksal") && !gehoert.includes("kampf") && !gehoert.includes("cantina") && !gehoert.includes("song") && !gehoert.includes("bar")) {
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

# Sicherer Python-Befehl: Setzt die Musik-Datenströme ohne f-String ein
html_bereit = html_reine_web_app.replace("PLATZHALTER_DUEL_MUSIC", duel_base64).replace("PLATZHALTER_CANTINA_MUSIC", cantina_base64).replace("PLATZHALTER_Hello_MUSIC", hello_base64).replace("PLATZHALTER_CLONE_MUSIC", clone_base64)


# Zeigt die fertige App blockierungsfrei auf Streamlit an
st.components.v1.html(html_bereit, height=270)
