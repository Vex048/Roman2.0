import speech_recognition as sr
from datetime import date
from time import sleep
from camera import opencv,returnValueFromHand
import tensorflow as tf
import settings
from server import startPlayback, stopPlayback,nextPlayback,prevPlayback,resumePlayback
import threading
# stop_threads = False


# settings.init()


# model_ = tf.keras.models.load_model("weights/mobilenetV3Large1.h5")
# t1 = threading.Thread(target=opencv,args=(lambda : stop_threads,model_))
# t2 = threading.Thread(target=serverS.run)
# t2.start()


def startSR(model):
    t1 = threading.Thread(target=opencv,args=(model,))
    r = sr.Recognizer()
    mic = sr.Microphone()

    print("hello")

    while True:
        with mic as source:
            audio = r.listen(source)
        try:
            words = r.recognize_google(audio)
            print(words)
          
            if words == "today":
                print(date.today())

            if words == "play music":
                if not t1.is_alive():
                    t1 = threading.Thread(target=opencv,args=(model,))
                    t1.start()
                startPlayback()
                


            if words == "stop music":
                settings.stop_threads = True
                t1.join()
                print("thread shoudl be down")
                stopPlayback()
                settings.started == False



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


# r = sr.Recognizer()
# mic = sr.Microphone()

# print("hello")

# while True:
#     with mic as source:
#         audio = r.listen(source)
#     try:
#         words = r.recognize_google(audio)
#         print(words)

#         if words == "today":
#             print(date.today())

#         if words == "play music":
#             if not t1.is_alive():
#                 stop_threads = False
#                 t1.start()
#             server.startPlayback()


#         if words == "stop music":
#             stop_threads = True
#             t1.join()
#             server.stopPlayback()

#         if words == "predict":
#             if settings.handValue == 0:
#                 print("FIST")
#             elif settings.handValue == 1:
#                 print("ONE")
#             elif settings.handValue == 2:
#                 print("PALM")
#             elif settings.handValue == 3:
#                 print("THREE")

#         if words == "exit":
#             print("...")
#             sleep(1)
#             print("...")
#             sleep(1)
#             print("...")
#             sleep(1)
#             print("Goodbye")
#             break
#     except:
#         print("speak again")