import re
import os
from pydub import AudioSegment
import io
import speech_recognition as sr
import platform

# Determina il sistema operativo
print(platform.system())
if platform.system() == 'Windows':
    ffmpeg_path = os.path.join(os.path.dirname(__file__), '..', '..', 'bin', 'ffmpeg.exe')  # Per Windows
    os.environ["PATH"] += os.pathsep + ffmpeg_path
elif platform.system() == 'Linux':
    ffmpeg_path = os.path.join(os.path.dirname(__file__), '..', '..', 'bin', 'ffmpeg')  # Per Linux
    os.environ["PATH"] += os.pathsep + ffmpeg_path
else:
    raise Exception("Sistema operativo non supportato.")

try:
    AudioSegment.ffmpeg = ffmpeg_path
except Exception as e:
    print(f"Errore durante il caricamento di ffmpeg: {e}")

recognizer = sr.Recognizer()

def detect_stuttering(text):
    """
    Analizza il testo per rilevare balbuzie, includendo ripetizioni di lettere, sillabe e parole.
    Calcola una percentuale di occorrenze.
    """
    words = text.split()
    total_words = len(words)
    if total_words == 0:
        return 0, [], [], []  # Se non ci sono parole, restituisci 0%

    # Modelli per rilevare ripetizioni di parole, sillabe, e lettere
    word_repeat_pattern = re.compile(r'\b(\w+)\s+\1\b', re.IGNORECASE)
    syllable_repeat_pattern = re.compile(r'\b(\w{1,3})-\1+', re.IGNORECASE)
    letter_repeat_pattern = re.compile(r'\b([a-zA-Z])[- ]?\1+', re.IGNORECASE)

    word_matches = word_repeat_pattern.findall(text)
    syllable_matches = syllable_repeat_pattern.findall(text.replace(" ", "-"))
    letter_matches = letter_repeat_pattern.findall(text.replace(" ", "-"))

    # Conta tutte le ripetizioni rilevate
    total_repeats = len(word_matches) + len(syllable_matches) + len(letter_matches)
    stutter_percentage = (total_repeats / total_words) * 100 if total_words > 0 else 0
    return stutter_percentage, word_matches, syllable_matches, letter_matches


def select_audio_file():
    """
    Mostra una finestra per selezionare un file audio.
    """
    from tkinter import Tk, filedialog
    Tk().withdraw()  # Nasconde la finestra principale di Tkinter
    file_path = filedialog.askopenfilename(
        title="Seleziona un file audio",
        filetypes=[("Audio Files", "*.wav *.mp3")],
    )
    return file_path


def process_audio_file(file_path):
    """
    Processa un file audio, esegue il riconoscimento vocale e rileva eventuali balbuzie.
    """
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension not in ['.mp3', '.wav']:
        print("Formato audio non supportato.")
        return
    
    # Usa pydub per caricare il file audio e convertirlo in WAV se necessario
    audio = AudioSegment.from_file(file_path)
    audio = audio.set_channels(1).set_frame_rate(16000)  # Converte a mono e 16kHz per il riconoscimento vocale

    # Converte l'audio in un buffer
    audio_bytes = io.BytesIO()
    audio.export(audio_bytes, format="wav")
    audio_bytes.seek(0)
    # Riconoscimento vocale con speech_recognition
    with sr.AudioFile(audio_bytes) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="it-IT")
        except sr.UnknownValueError:
            print("Impossibile riconoscere l'audio.")
            return
        except sr.RequestError as e:
            print(f"Errore di richiesta: {e}")
            return
        
        print(f"Testo riconosciuto: {text}")
         # Rilevamento della balbuzie nel testo
        stutter_percentage, word_matches, syllable_matches, letter_matches = detect_stuttering(text)
          # Crea un dizionario con le chiavi e i rispettivi valori
        data = {
                "stutter_percentage": stutter_percentage,
                "word_matches": word_matches,
                "syllable_matches": syllable_matches,
                "letter_matches": letter_matches
            }

        if stutter_percentage <= 0:
            print("Nessuna balbuzie rilevata.")
            return data
        
        print(f"Balbuzie rilevata nel testo: {stutter_percentage:.2f}%")
        if word_matches:
            print(f"Ripetizioni di parole: {word_matches}")
        if syllable_matches:
            print(f"Ripetizioni di sillabe: {syllable_matches}")
        if letter_matches:
            print(f"Ripetizioni di lettere: {letter_matches}")
        
        return data
            
        
"""
DEBUG ONLY
# Seleziona il file audio e processalo
audio_file = select_audio_file()

if platform.system() == 'Windows':
    os.system('cls')
else:
    os.system('clear')
    
if audio_file:
    process_audio_file(audio_file)
else:
    print("Nessun file selezionato.")
"""