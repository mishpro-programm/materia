import os
from time import sleep
from threading import Thread
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
        print(bar[i % len(bar)], end='\r')
        sleep(0.1)
        i += 1
    print("Готово     ")
print("\033[33mУстановка скрипта...\033[0m")
done = False
tInstall = Thread(target=loading)
tInstall.start()
os.popen("pip install -r requirements.txt").read()
done = True
sleep(0.2)
import main
