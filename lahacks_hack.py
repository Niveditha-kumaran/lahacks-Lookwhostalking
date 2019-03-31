import pyaudio
import wave

from pydub import AudioSegment
import os
import io
from google.cloud import speech

from google.cloud.speech import enums as enums_speech
from google.cloud.speech import types as types_speech

from google.cloud import language
from google.cloud.language import enums as enums_language
from google.cloud.language import types as types_language
import sys
import numpy as np
import glob
import collections
from collections import Counter, defaultdict
import re
import json
import math
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

def query_api():

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 10
    WAVE_OUTPUT_FILENAME = "voice.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


    audio = AudioSegment.from_wav("voice.wav")

    audio.export('voice.flac', format= "flac")



    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "D:\\USC\\LAHacks\\lahacks-2019-speech-f1e3cbb958e2.json"



    #Initialize the speech client instance to access the Speech-to-Text API
    client = speech.SpeechClient()

    file_name = os.path.join(os.getcwd(), 'voice.flac')
    # audio = types.RecognitionAudio(file_name)

    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types_speech.RecognitionAudio(content=content)

    config = types_speech.RecognitionConfig(
        encoding=enums_speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz = 44100,
        language_code = 'en-US')

    response = client.recognize(config, audio)

    text = ""

    result = {}

    for result in response.results:
        print(result.alternatives[0])
        text += result.alternatives[0].transcript

    client = language.LanguageServiceClient()

    text = text[0].upper() + text[1:]

    document = types_language.Document(content=text, type=enums_language.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(document=document).document_sentiment

    nbmodel= open("emo.txt","r")
    temp= nbmodel.readline()
    #classes
    classes=[]
    for _ in range(5):
        classes.append(nbmodel.readline()[:-1])

    tempv=nbmodel.readline()
    vocabline=nbmodel.readline()
    #vocab
    vocablist= vocabline.split(" ")
    vocablist= vocablist[:-1]
    #print((vocablist[-1]))
    #priors
    priorline= nbmodel.readline()
    jpriors= eval(priorline)


    cpline= nbmodel.readline()
    jcp= eval(cpline,{})




    stopWords = set(stopwords.words('english'))
    sentence= text

    flets=list(re.findall(r'\w+',sentence.lower()))
    templist=[]
    for f1 in flets:
            if f1 not in stopWords and f1.isalpha():
                templist.append(f1)
    #print(templist)   
    if len(templist)< (len(flets)/4) or len(templist)<=5:
        toks= flets
    else:
        toks= templist
    #print(toks)

     
    neww=[x for x in toks if x in vocablist]
    scores=[0.0 for _ in range(5)]
    for i in range(len(classes)):
        scores[i]= math.log(jpriors[classes[i]])
        for terms in neww:
            scores[i] += math.log(jcp[terms+'/'+classes[i]])
    #print(scores)
        

    final = [math.exp(score) for score in scores]

    final = [round(score/sum(final)*100,2) for score in final]

    result = defaultdict(float)

    for c in range(len(classes)):
        result[classes[c]]=final[c]

    return final[0], final[1], final[2], final[3], final[4], sentence, round(sentiment.magnitude,2), round(sentiment.score,2), round(len(text.split(" "))/RECORD_SECONDS*60,1)
