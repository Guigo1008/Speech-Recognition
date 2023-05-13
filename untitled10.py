from googletrans import Translator
import speech_recognition as sr
import threading
import queue
import re
from pydub import AudioSegment
from pydub.silence import split_on_silence
from io import BytesIO

def split_words(text):
    return text.split()

def traduzir_texto(text_queue, translated_text_queue):
    tradutor = Translator()
    while True:
        texto = text_queue.get()
        if texto is None:
            break
        palavras = split_words(texto)
        for palavra in palavras:
            resultado = tradutor.translate(palavra, src='pt', dest='en')
            translated_text_queue.put(resultado.text)
        translated_text_queue.put(None)

def callback(recognizer, audio):
    try:
        audio_data = audio.get_wav_data()
        audio_segment = AudioSegment.from_wav(BytesIO(audio_data))
        chunks = split_on_silence(audio_segment, min_silence_len=100, silence_thresh=-40)
        for chunk in chunks:
            chunk_data = chunk.export(format="wav")
            chunk_audio = sr.AudioData(chunk_data.read(), audio.sample_rate, audio.sample_width)
            resultado = recognizer.recognize_google(chunk_audio, language='pt')
            text_queue.put(resultado)
    except sr.UnknownValueError:
        pass

def exibir_traducao(translated_text_queue):
    while True:
        texto_traduzido = translated_text_queue.get()
        if texto_traduzido is None:
            break
        print(f'Traduzido para o inglês: {texto_traduzido}')

audio = sr.Recognizer()
text_queue = queue.Queue()
translated_text_queue = queue.Queue()

try:
    source = sr.Microphone()
    ouvir_thread = threading.Thread(target=audio.listen_in_background, args=(source, callback))
    traduzir_thread = threading.Thread(target=traduzir_texto, args=(text_queue, translated_text_queue))
    exibir_thread = threading.Thread(target=exibir_traducao, args=(translated_text_queue,))

    ouvir_thread.start()
    traduzir_thread.start()
    exibir_thread.start()

    ouvir_thread.join()
    traduzir_thread.join()
    exibir_thread.join()
except Exception as e:
    print(f'Erro no áudio: {e}')