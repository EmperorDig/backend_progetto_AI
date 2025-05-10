import re
import os
from pydub import AudioSegment
import io
import speech_recognition as sr
import platform
import tempfile
import random   # Importa per la generazione casuale
import string   # Importa per i set di caratteri (lettere, numeri)

# ... (il tuo setup di ffmpeg, recognizer e le funzioni detect_stuttering, select_audio_file) ...

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


# ... (importazioni, setup ffmpeg, recognizer, detect_stuttering, select_audio_file) ...

def process_audio_file(file_path):
    """
    Processa un file audio (inclusi M4A, MP3, WAV), converte in un formato compatibile,
    salva il risultato finale in MP3 con un nome casuale,
    esegue il riconoscimento vocale e rileva eventuali balbuzie.
    """
    file_extension = os.path.splitext(file_path)[1].lower()
    # Estrai il nome base del file e la directory di origine
    original_filename_base = os.path.splitext(os.path.basename(file_path))[0]
    original_directory = os.path.dirname(file_path)

    supported_extensions = ['.mp3', '.wav', '.m4a']
    if file_extension not in supported_extensions:
        print(f"Formato audio non supportato: {file_extension}. Formati supportati: {', '.join(supported_extensions)}")
        return None

    original_file_path = file_path
    temp_mp3_file = None
    output_mp3_path = None

    try:
        # Carica il file audio con pydub (gestisce M4A, MP3, WAV)
        audio = AudioSegment.from_file(original_file_path)

        # Se il file originale è M4A, gestisci la conversione temporanea se necessario per l'elaborazione
        # (Anche se ora salviamo il risultato finale, questa conversione intermedia potrebbe essere utile
        # per la compatibilità con il caricamento successivo da file se l'elaborazione lo richiedesse,
        # anche se la logica attuale carica direttamente dall'oggetto audio in memoria per la seconda fase).
        # Manteniamo la logica esistente per chiarezza nel processo di conversione.
        if file_extension == '.m4a':
            print("Conversione M4A a MP3 temporaneo per elaborazione...")
            temp_mp3_file = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
            temp_mp3_path = temp_mp3_file.name
            temp_mp3_file.close()

            # Esporta l'audio in formato MP3 temporaneo
            audio.export(temp_mp3_path, format="mp3")
            # ATTENZIONE: Qui stiamo ancora puntando file_path al file temporaneo.
            # Se la logica successiva carica da file_path, userà il temporaneo.
            # Se invece usa l'oggetto 'audio' in memoria, non dipende da file_path.
            # La logica attuale per speech_recognition usa l'oggetto 'audio' in memoria,
            # quindi il puntamento di file_path qui è meno critico per la fase successiva,
            # ma lo manteniamo per coerenza con la logica precedente.
            file_path = temp_mp3_path


        # --- NUOVA LOGICA: SALVA IL FILE FINALE IN MP3 CON NOME CASUALE ---
        # Definisci la lunghezza della stringa casuale
        random_string_length = 12 # Puoi regolare la lunghezza come preferisci

        # Genera una stringa casuale di lettere (maiuscole e minuscole) e cifre
        random_chars = string.ascii_letters + string.digits
        random_name_suffix = ''.join(random.choices(random_chars, k=random_string_length))

        # Genera il nome per il file MP3 di output usando il nome originale + suffisso casuale
        output_filename = f"{original_filename_base}_{random_name_suffix}.mp3"
        # Definisci il percorso completo dove salvare il file MP3 processato
        # Lo salviamo nella stessa directory del file originale.
        output_mp3_path = os.path.join(original_directory, output_filename)
        print(f"Salvataggio del file processato in: {output_mp3_path}")

        # Esporta l'oggetto AudioSegment caricato (che rappresenta l'audio) nel file MP3 di output
        # Indipendentemente dal formato di input, l'oggetto 'audio' contiene i dati audio caricati.
        try:
             audio.export(output_mp3_path, format="mp3")
             print("File MP3 processato salvato con successo.")
        except Exception as e:
             print(f"Errore durante il salvataggio del file MP3 processato: {e}")
             # Decidi come gestire questo errore: potresti voler sollevare un'eccezione
             # o restituire un risultato con un errore specifico.
             # Per ora, stampiamo e continuiamo con il riconoscimento vocale se possibile.


        # --- Logica Esistente per Riconoscimento Vocale (opera su buffer WAV in memoria) ---
        # Converte l'audio (dall'AudioSegment caricato 'audio') in un formato compatibile
        # con speech_recognition (mono, 16kHz WAV) - questo è per l'elaborazione in memoria.
        # Usiamo l'oggetto 'audio' che è stato caricato da AudioSegment.from_file()
        audio_for_recognition = audio.set_channels(1).set_frame_rate(16000)

        # Converte l'audio in un buffer WAV in memoria per speech_recognition
        audio_bytes = io.BytesIO()
        audio_for_recognition.export(audio_bytes, format="wav")
        audio_bytes.seek(0)

        # Riconoscimento vocale con speech_recognition
        with sr.AudioFile(audio_bytes) as source:
            audio_data = recognizer.record(source)
            try:
                print("Eseguo riconoscimento vocale...")
                text = recognizer.recognize_google(audio_data, language="it-IT")
                print(f"Testo riconosciuto: {text}")

                # Rilevamento della balbuzie nel testo
                stutter_percentage, word_matches, syllable_matches, letter_matches = detect_stuttering(text)

                data = {
                    "stutter_percentage": stutter_percentage,
                    "word_matches": word_matches,
                    "syllable_matches": syllable_matches,
                    "letter_matches": letter_matches,
                    "processed_mp3_path": output_mp3_path
                }

                return data # Restituisce il dizionario dei risultati (incluso il percorso MP3)

            except sr.UnknownValueError:
                print("Impossibile riconoscere l'audio.")
                return {"error": "Impossibile riconoscere l'audio"}
            except sr.RequestError as e:
                print(f"Errore di richiesta al servizio di riconoscimento vocale: {e}")
                return {"error": f"Errore di riconoscimento vocale: {e}"}

    except Exception as e:
        # Cattura eventuali altri errori durante il caricamento, l'esportazione o l'elaborazione
        print(f"Errore generale durante l'elaborazione audio: {e}")
        return {"error": f"Errore elaborazione audio: {e}"}

    finally:
        # Pulisci il file temporaneo MP3 se è stato creato per la conversione iniziale M4A
        if temp_mp3_file and os.path.exists(temp_mp3_path):
            print(f"Pulizia file temporaneo M4A convertito: {temp_mp3_path}")
            os.remove(temp_mp3_path)
     
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



#Gestire i file di input nei formati .mp3, .wav, .m4a.
#Se il file è .m4a, convertirlo temporaneamente in MP3 per l'elaborazione interna.
#Caricare l'audio usando pydub.AudioSegment.
#Salvare la versione finale dell'audio caricato in formato MP3 nella stessa directory del file originale, con un nome file che include una stringa casuale.
#Preparare l'audio per speech_recognition (convertendolo in un buffer WAV mono 16kHz in memoria).
#Eseguire il riconoscimento vocale.
#Eseguire l'analisi della balbuzie sul testo riconosciuto.
#Restituire un dizionario con i risultati, incluso il percorso del file MP3 salvato.
#Pulire il file MP3 temporaneo creato solo per la conversione iniziale da M4A (se applicabile).