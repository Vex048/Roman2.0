import speech_recognition as sr
from datetime import date
from time import sleep
from camera import opencv
import tensorflow as tf
import settings
import sounddevice
from server import startPlayback, stopPlayback,nextPlayback,prevPlayback,resumePlayback,choosePlaylist,setVolume
import threading
import os
import board
import adafruit_bmp280
import adafruit_dht
import JokesMaker
from word2number import w2n
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)


dht_device=adafruit_dht.DHT11(board.D4, use_pulseio=False)

i2c=board.I2C()
bmp280=adafruit_bmp280.Adafruit_BMP280_I2C(i2c,address=0x76)
bmp280.sea_level_pressure=1013.25


def startSR(model):
    t1 = threading.Thread(target=opencv,args=(model,))
    r = sr.Recognizer()
    mic = sr.Microphone()
    jokeMaker=JokesMaker.JokesMaker()
    print("hello")

    while True:
        with mic as source:
            audio = r.listen(source)
        try:
            words = r.recognize_google(audio)
            print("Understood words: ",words)
          
            if words == "today":
                print(date.today())

            elif words == "hello":
                message ="  Hello"
                os.system("espeak '"+message+"'  -s 150")
            elif words == "thank you" or words =="thanks":
                message = "  Your welcome"
                os.system("espeak  '"+message+"'  -s 150")

            elif words == "play music" and settings.currToken!=None:
                if not t1.is_alive():
                    t1 = threading.Thread(target=opencv,args=(model,))
                    t1.start()
                    print("Loading camera ...")
                startPlayback()                
            elif words == "stop music" and settings.currToken!=None:
                settings.stop_threads = True
                t1.join()
                print("Thread finished")
                stopPlayback()
                settings.started = False

            elif words == "temperature":
                try:
                   temperature=dht_device.temperature
                   message = f"Current temperature totals {temperature} Celcius"
                   os.system("espeak '"+message+"' -s 150 ")
                except RuntimeError:
                   temperature = bmp280.temperature
                   message = f"Current temperature totals {temperature} Celcius"
                   os.system("espeak '"+message+"' -s 150")
            elif words == "humidity":
                humidity=dht_device.humidity
                message = f"Current humidity totals {humidity} percent"
                os.system("espeak '"+message+"' -s 150")
            elif words == "pressure":
                pressure =  bmp280.pressure
                pressure = "{:.2f}".format(pressure)
                message = f"Current pressure totals  {pressure}  hecto Pascals"
                os.system("espeak '"+message+"' -s 150 ")
            elif words == "turn on light":
               GPIO.output(18,GPIO.HIGH)
            elif words == "turn off light":
               GPIO.output(18,GPIO.LOW)

            elif words == "make joke" or words == "make a joke":
                x= jokeMaker.generateRandom()
                joke = "    "+jokeMaker.getJoke(x)
                os.system("espeak '"+joke+"'  -s 150 ")

            elif (words == "choose playlist" or words =="truth playlist") and settings.currToken!=None:
                while True:
                   with mic as source:
                      audio2 = r.listen(source)
                      try:
                         print("Select playlist")
                         num = r.recognize_google(audio2)
                         num=num.split(" ")
                         print("You chose playlist number: ",num[1])
                         if len(num) != 2:
                            break
                         choosePlaylist(changeWordToNum(num[1]))
                         break
                      except sr.UnknownValueError:
                         message = "     You have chosen a wrong number"
                         os.system("espeak '"+message+"' -s 150")
                         break
                      except:
                         print("Couldnt load playlist")
                         break 

            elif wordsSplitVolume(words) == "set volume" and settings.currToken!=None:
                     vol = getVolume(words)
                     print(vol)
                     setVolume(vol)
                     
            elif words == "exit":
                print("...")
                sleep(1)
                print("...")
                sleep(1)
                print("...")
                sleep(1)
                print("Goodbye")
                os._exit(1)
                break
        except sr.UnknownValueError:
            print("speak again")

def changeWordToNum(word):
   return w2n.word_to_num(word)

def wordsSplitVolume(word):
   wordList=word.split(" ")
   if len(wordList) != 3:
      return 0
   words = wordList[0]+" "+wordList[1]
   volume = wordList[2]
   return words
def getVolume(word):
   wordList = word.split(" ")
   return wordList[2]
