import streamlit as st
import speech_recognition as sr
import io

st.set_page_config(page_title="Garmin Assistent", page_icon="🎙️")
st.title("🎙️ Garmin Echtzeit-Assistent")

st.write("Drücke auf das Mikrofon, sprich deinen Befehl und drücke auf Stop:")

# Der offizielle, eingebaute Mikrofon-Button von Streamlit
audio_file = st.audio_input("Sprachbefehl aufnehmen")

# Wenn eine Aufnahme vorliegt, verarbeite sie direkt in Python
if audio_file:
    recognizer = sr.Recognizer()
    
    try:
        # Die Aufnahme für die Spracherkennung vorbereiten
        audio_bytes = audio_file.read()
        with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
            audio_data = recognizer.record(source)
        
        # Sprache in Text umwandeln
        text = recognizer.recognize_google(audio_data, language="de-DE").lower()
        st.write(f"**Gehört:** '{text}'")
        
        # Verarbeitung deiner Befehle
        antwort = ""
        
        # Variante 1: Alles in einem Satz ("Okay Garmin Hallo")
        # Variante 2: Nur der Befehl ("Hallo"), falls du vorher manuell aktiviert hast
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
            st.info("Du kannst das Browser-Tab jetzt schließen.")

        # Wenn eine Antwort da ist, lässt Python den Webbrowser laut sprechen
        if antwort:
            js_speech = f"""
            <script>
            const speech = new SpeechSynthesisUtterance('{antwort}');
            speech.lang = 'de-DE';
            window.speechSynthesis.speak(speech);
            </script>
            """
            st.components.v1.html(js_speech, height=0, width=0)

    except sr.UnknownValueError:
        st.error("Audio erhalten, aber ich konnte kein deutliches Wort verstehen.")
    except Exception as e:
        st.error("Fehler bei der Verarbeitung. Bitte noch einmal versuchen.")
