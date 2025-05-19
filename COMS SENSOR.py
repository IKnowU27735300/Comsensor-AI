import pyaudio
import wave
import speech_recognition as sr
import os
import pydub
from pydub import AudioSegment
from gtts import gTTS

# Constants
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
WAVE_OUTPUT_FILENAME = "output.wav"  # Changed to .wav
BEEP_SOUND_FILENAME = "beep.wav"

def record_audio():
    """Record audio and save as MP3"""
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")
    frames = []

    while True:
        try:
            data = stream.read(CHUNK)
            frames.append(data)
        except KeyboardInterrupt:
            print("* done recording")
            break
        except Exception as e:
            print(f"Error: {e}")
            return None

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save as WAV temporarily
    wf = wave.open("temp.wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    # Convert WAV to MP3
    sound = AudioSegment.from_wav("temp.wav")
    sound.export(WAVE_OUTPUT_FILENAME, format="mp3")

    # Remove temporary WAV file
    os.remove("temp.wav")

    return WAVE_OUTPUT_FILENAME

def speech_to_text(mp3_file):
    """Convert MP3 to text using speech recognition"""
    # Convert MP3 to WAV
    AudioSegment.from_mp3(mp3_file).export("temp.wav", format="wav")

    r = sr.Recognizer()
    try:
        with sr.AudioFile("temp.wav") as source:
            audio = r.record(source)
            text = r.recognize_google(audio, language="en-US")
            return text
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio")
        return ""
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        os.remove("temp.wav")  # Ensure the temp file is always deleted

def remove_censored_words(text, censored_words):
    """Remove censored words from text"""
    return " ".join([word for word in text.split() if word.lower() not in censored_words])

def text_to_speech(text, output_file="output_censored.mp3"):
    """Convert text to speech"""
    try:
        tts = gTTS(text=text, lang='en')
        tts.save(output_file)
        return output_file
    except Exception as e:
        print(f"Error: {e}")
        return None

def add_beep_sound(mp3_file, beep_file, censored_words, original_text):
    """Add beep sound to censored parts"""
    try:
        if not os.path.exists(beep_file):
            print(f"Error: Beep sound file '{beep_file}' does not exist.")
            return None
        
        beep_sound = AudioSegment.from_wav(beep_file)
        audio_censored = AudioSegment.from_mp3(mp3_file)
        start = 0
        
        for word in original_text.split():
            if word.lower() in censored_words:
                start_time = original_text.lower().find(word.lower(), start)
                end_time = start_time + len(word)
                start = end_time  # Update start to avoid repeated words
                position = start_time * 1000  # Convert position to milliseconds
                audio_censored = audio_censored.overlay(beep_sound, position=position)

        audio_censored.export("output_censored_beep.mp3", format="mp3")
        return "output_censored_beep.mp3"
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    while True:
        print("1. Go Live")
        print("2. End Live")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            censored_words_input = input("Enter censored words separated by commas: ")
            censored_words = [word.strip() for word in censored_words_input.split(",")]  # Dynamic input for censored words

            # Step 1: Record audio
            mp3_file = record_audio()
            if mp3_file is None:
                print("Error: Failed to record audio.")
                continue

            # Step 2: Convert recorded audio to text
            text = speech_to_text(mp3_file)
            if text is None:
                print("Error: Failed to convert speech to text.")
                continue

            print("Original Text:", text)

            # Step 3: Censor the text by removing censored words
            text_censored = remove_censored_words(text, censored_words)
            print("Censored Text:", text_censored)

            # Step 4: Convert censored text to speech
            mp3_censored_file = text_to_speech(text_censored)
            if mp3_censored_file is None:
                print("Error: Failed to convert text to speech.")
                continue

            # Step 5: Add beep sound to the original text for censored words
            final_mp3 = add_beep_sound(mp3_censored_file, BEEP_SOUND_FILENAME, censored_words, text)
            if final_mp3 is None:
                print("Error: Failed to add beep sounds.")
                continue

            print("Final censored audio with beeps saved as:", final_mp3)

        elif choice == '2':
            print("Ending live session.")
            break
        elif choice == '3':
            print("Exiting.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
