import requests
import json
from datetime import datetime
import smtplib

## Costant declaration
ISS_API = "http://api.open-notify.org/iss-now.json"
SUN_RISE_SET_API = " https://api.sunrise-sunset.org/json"
MY_LAT = 50.643910
MY_LONG = 5.571560

EMAIL = " "
APP_KEY = ""
RECEIVER_EMAIL = ""

## Variable
iss_latitude = None
iss_longitude = None


#ISS overhead, return true longitude and latitude are in the range of +-5°
def iss_overhead():
    iss_response = requests.get(ISS_API)
    iss_data = iss_response.json()
    
    ISS_LAT = iss_data["iss_position"]["latitude"]
    ISS_LONG = iss_data["iss_position"]["longitude"]
    
    global iss_latitude 
    global iss_longitude 
    iss_latitude = ISS_LAT
    iss_longitude = ISS_LONG

    if (MY_LAT -5 <= float(ISS_LAT) <= MY_LAT +5) and (MY_LONG -5 <= float(ISS_LONG) <= MY_LONG +5):
        return True


#SUNRISE SUNSET API
def is_night():
    parameters = {
        "lat": MY_LAT,
        "long": MY_LONG,
        "formated": 0,
    }
    response = requests.get(url=SUN_RISE_SET_API, params=parameters)
    response.raise_for_status()
    data = response.json()

    sunrise = data["results"]["sunrise"]
    sunset = data["results"]["sunset"]

    sunrise_hour =int( ((sunrise.split(" "))[0].split(":"))[0] )
    sunset_hour = int( ((sunset.split(" "))[0].split(":"))[0] )

    current_hour = datetime.now().hour
    day = datetime.now().day

    if current_hour >= sunset_hour or current_hour <= sunrise_hour:
        return True
    
registro = {}

def send_email():
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=APP_KEY)
        connection.sendmail(from_addr=EMAIL, to_addrs=RECEIVER_EMAIL, msg=f"Subject:hey! look up, you may see the ISS\n\nlook up, you may see the ISS")
    
    nuova_voce = { "iss was intercepted":
    {"date": datetime.now(),
    "iss latitude": iss_latitude,
    "iss longitude": iss_longitude,
    "status": "iss over the geo-location you insert"}
    }

    with open("./registro.json", "w") as file:
        json.dump(nuova_voce, file, indent=4)

prg_on = True

while prg_on:
    if iss_overhead() and is_night():
        send_email()

    print("procceess")