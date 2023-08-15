from pyrogram import Client, errors, filters
import schedule
from threading import Thread
from time import sleep
import os
import signal

def sigint(_, __):
    if 'materia.session' in os.listdir():
        os.remove('materia.session')
    print("\033[31mОтмена\033[0m")
    exit(1)
signal.signal(signal.SIGINT, sigint)
bar = [
    "[=     =]",
    "[==     ]",
    "[ ==    ]",
    "[  ==   ]",
    "[   ==  ]",
    "[    == ]",
    "[     ==]"
]
done = False
def loading():
    i = 0
    while not done:
        print(bar[i % len(bar)], end="\r")
        i+=1
        sleep(0.1)
    print("Готово    ")
    return
api_id = 24851427
api_hash = 'b73fb7bae6362ba5d37825d8334ec903'

app = Client("materia", api_id, api_hash, "Materia 1.0", "@mishpro Scripts")

def auth():
    global done
    print("\033[33mПодключение...\033[0m")
    done = False
    tConnect = Thread(target=loading)
    tConnect.start()
    app.connect()
    done = True
    sleep(0.1)
    print("\033[33mИнициализация...\033[0m")
    done = False
    tInitialize = Thread(target=loading)
    tInitialize.start()
    app.initialize()
    done = True
    sleep(0.2)
    phone_number = input("\033[33mВведите номер телефона: \033[0m")
    app.phone_number = phone_number
    try:
        code = app.send_code(phone_number)
    except errors.PhoneNumberInvalid:
        print("\033[31mНеверный номер телефона!\033[0m")
        if 'materia.session' in os.listdir():
            os.remove('materia.session')
        exit(1)
    phone_code = input("\033[33mВведите код из телеграма: \033[0m")
    try:
        app.sign_in(phone_number, code.phone_code_hash, phone_code)
        app.phone_code = phone_code
    except errors.PhoneCodeInvalid:
        print("\033[31mНеверный код!\033[0m")
        if 'materia.session' in os.listdir():
            os.remove('materia.session')
        exit(1)
    except errors.SessionPasswordNeeded:
        password = input(f"\033[33mВведите пароль (Подсказка: {app.get_password_hint()}): \033[0m")
        try:
            app.check_password(password)
            app.password = password
            print("\033[33mАвторизация удалась!")
        except errors.PasswordHashInvalid:
            print("\033[31mНеверный пароль!\033[0m")
            app.log_out()
            if 'materia.session' in os.listdir():
                os.remove('materia.session')
            exit(1)
if "materia.session" in os.listdir():
    try:
        app.start()
        print("\033[33mВход не требуется\033[0m")
    except Exception:
        print("\033[33mНеобходимо войти\033[0m")
        os.remove("materia.session")
        auth()
else:
    print("\033[33mНеобходимо войти\033[0m")
    auth()
def kopat():
    app.send_message("bforgame_bot", "Копать материю")
    print("+1")
schedule.every(8).minutes.do(kopat)
kopat()
while True:
    schedule.run_pending()
    sleep(0.5)
