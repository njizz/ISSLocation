import requests
import smtplib
import time
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv("config.env")

MY_LAT = 51.488991  # Your latitude
MY_LONG = -2.607281  # Your longitude
MY_EMAIL = os.getenv("MY_EMAIL")
APP_PWD = os.getenv("APP_PWD")


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if abs(iss_latitude - MY_LAT) <= 5 and abs(iss_longitude - MY_LONG) <= 5:
        print(iss_latitude, iss_longitude)
        print(MY_LAT, MY_LONG)
        print("the iss is overhead")
        return True
    else:
        print(iss_latitude, iss_longitude)
        print(MY_LAT, MY_LONG)
        print("the iss is NOT overhead")
        return False


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()

    if time_now.hour >= sunset or time_now.hour <= sunrise:
        print("it is night")
        return True
    else:
        print("it is NOT night")
        return False


start_time = time.time()
while True:
    if is_night() and is_iss_overhead():
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=APP_PWD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg=f"Subject:LOOK UP!\n\nThe ISS is in the sky above you!"
            )
    time.sleep(60.0 - ((time.time() - start_time) % 60.0))





