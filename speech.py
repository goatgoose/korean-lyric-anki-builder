from gtts import gTTS, lang

tts = gTTS('하루종일', lang='ko')
tts.save('hello.mp3')
