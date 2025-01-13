import speech_recognition as sr
from datetime import date
from time import sleep
import sounddevice
import os
r = sr.Recognizer()
mic = sr.Microphone()

print("hello")

while True:
    print("JOl")
    with mic as source:
        audio = r.listen(source)
    try:
        words = r.recognize_google(audio)
        print(words)
        
        if words == "today":
            print(date.today())

        if words == "Get current temperature":
            pass
            #temp,humidity = sensors.request()
            #os.system("espeak '"+today+"' ")
            
        if words == "Get current humidity":
            #temp,humidity = sensors.request()
            #os.system("espeak '"+humidity+"' ")
            pass
        if words == "Get current pressure":
            text = "Current pressure totals " 
            #pressure = sensorPressure.get()
            #text=text+pressure
            #os.system("espeak '"+text+"' ")
            pass




        if words == "exit":
            print("...")
            sleep(1)
            print("...")
            sleep(1)
            print("...")
            sleep(1)
            print("Goodbye")
            break
    except sr.UnknownValueError:
        print("speak again")
