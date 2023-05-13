import queue
import threading
from googletrans import Translator
import speech_recognition as sr

def traduzir_texto(text_queue, translated_text_queue):
    tradutor = Translator()
    while True:
        texto = text_queue.get()
        if texto is None:
            break
        resultado = tradutor.translate(texto, src='pt', dest='en')
        translated_text_queue.put(resultado.text)

def ouvir_e_reconhecer(audio, source, text_queue):
    while True:
        # input('Aperte enter para traduzir: ')
        print('Ouvindo...')
        voz = audio.record(source, duration=5)
        try:
            resultado = audio.recognize_google(voz, language='pt')
            text_queue.put(resultado)
        except sr.UnknownValueError:
            pass
        except KeyboardInterrupt:
            text_queue.put(None)
            break

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
    with sr.Microphone() as source:
        ouvir_thread = threading.Thread(target=ouvir_e_reconhecer, args=(audio, source, text_queue))
        traduzir_thread = threading.Thread(target=traduzir_texto, args=(text_queue, translated_text_queue))
        exibir_thread = threading.Thread(target=exibir_traducao, args=(translated_text_queue,))
        ouvir_thread.start()
        traduzir_thread.start()
        exibir_thread.start()
        ouvir_thread.join()
        traduzir_thread.join()
        exibir_thread.join()
except:
    print('Deu ruim no áudio.')