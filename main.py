from typing import Union

from fastapi import FastAPI, Request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

from provider.twilio import TwilioHandler
from provider.database import USER, ACTIVITY, FORMULIR, LAPORAN

twilio = TwilioHandler()

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/message")
async def message_handler(req: Request):
    # Parse incoming Twilio request
    print("++++++++++++++++++++++++++++++++++++++++++")
    twilio_data = await req.form()
    print(twilio_data)
    userNumber = twilio_data.get("From","")
    msg = twilio_data.get("Body","")
    profilName = twilio_data.get("ProfileName", "User")

    # Kita Cek Apakah User sudah ada di db
    if userNumber in USER:
        print("User ditemukan")
    else:
        print("User tidak ditemukan")
        USER[userNumber]= {
            "phoneNumber": userNumber,
        }

    # Kita Cek Aktivitas User
    if userNumber in ACTIVITY:
        print("Ada aktivitas")
        status = ACTIVITY[userNumber]
        print("Current act => ",status.get("activity"))

        match status.get("activity"):
            case "REGISTER":
                USER[userNumber]["profileName"] = msg
                twilio.sendMsg(userNumber, f"Hallo {msg} kami senang anda di sini")
                ACTIVITY[userNumber]["activity"] = "ASKING_FOR_SERVICE"
                twilio.sendMsg(userNumber, f"Apa yang bisa kami bantu? \n 1. Membuat Formulir \n 2. Laporkan Masalah \n *balasa hanya dengan angka")
            case "ASKING_FOR_SERVICE":
                print(msg)
                ACTIVITY[userNumber]["activity"] = f"SERVICE_{msg}"
                if msg == "1":
                    twilio.sendMsg(userNumber, f"Di mana alamat rumah anda?")
                if msg == "2":
                    twilio.sendMsg(userNumber, f"Apa masalah anda?")
            case "SERVICE_1":
                FORMULIR[userNumber] = {
                    "Nama_Dokumen":"Surat Keterangan",
                    "Nama_Pemohon": USER[userNumber]["profileName"],
                    "Alamat_Pemohon": msg,
                    "Deskripsi": "Dengan ini menyatakan"
                }
                twilio.sendMsg(userNumber, f"Berikut furmulir anda {FORMULIR[userNumber]}")
                ACTIVITY[userNumber]["activity"] = "NO_ACT"
            case "SERVICE_2":
                FORMULIR[userNumber] = {
                    "Nama_Dokumen":"Surat Masalah",
                    "Nama_Pemohon": USER[userNumber]["profileName"],
                    "Detail_Masalah": msg
                }
                twilio.sendMsg(userNumber, f"Berikut masalah anda {FORMULIR[userNumber]}")
                ACTIVITY[userNumber]["activity"] = "NO_ACT"
            case "NO_ACT":
                ACTIVITY[userNumber]["activity"] = "ASKING_FOR_SERVICE"
                twilio.sendMsg(userNumber, f"Apa yang bisa kami bantu? \n 1. Membuat Formulir \n 2. Laporkan Masalah \n *balasa hanya dengan angka")
            
    else:
        # Kalau belum ada aktivitas maka aktivitas awal adalah registering
        print("tidak ada aktivitas")
        ACTIVITY[userNumber]= {
            "phoneNumber": userNumber,
            "activity": "REGISTER",
            "detail": None
        }
        twilio.sendMsg(userNumber, f"Hallo selamat datang {profilName} di sistem kami, bagaimana kami harus menyapa anda?")




    # Return TwiML XML response
    return {"success": True}