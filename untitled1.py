import speech_recognition as sr

audio = sr.Recognizer()

try:
    with sr.Microphone() as source:
        while True:
            print('Ouvindo...')
            voz = audio.listen(source)
            resultado = audio.recognize_google(voz, language='pt-BR')
            print(f'Você disse: {resultado}')
except:
    print('Deu ruim no áudio.')