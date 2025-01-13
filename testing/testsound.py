from time import strftime
import os
import datetime
whole_date = strftime("%d/%m/%y at %I %M%p")

today = datetime.datetime.now().strftime(" %B %d %Y")
date = "Current date is" + today 
text = "Hello Martin, how are you doing today"
os.system("espeak '"+date+"' -s 150 ")
num = 23.5
numbers = f"The temperature totals: {num} Celcius"
os.system("espeak '"+numbers+"' -s 150 ")
