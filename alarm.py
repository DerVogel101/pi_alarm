# alarm.py

import RPi.GPIO as GPIO
import time
from datetime import datetime, timedelta
import ast

# Setzen Sie den Pin-Modus
GPIO.setmode(GPIO.BCM)

# Geben Sie die Pin-Nummer des Relais an
RELAY_PIN = 5

# Setzen Sie den Pin als Ausgang
GPIO.setup(RELAY_PIN, GPIO.OUT)

# Geben Sie die Pin-Nummer des Tasters an
BUTTON_PIN = 6

# Setzen Sie den Pin als Eingang mit Pull-up-Widerstand
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Geben Sie die Pin-Nummer des Tasters zum Aktivieren der Snooze-Funktion an
SNOOZE_BUTTON_PIN = 13

# Setzen Sie den Pin als Eingang mit Pull-up-Widerstand
GPIO.setup(SNOOZE_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Geben sie die pin-nummer der snooze-lampe an
SNOOZE_LED_PIN = 19

# Setzen Sie den Pin als Ausgang
GPIO.setup(SNOOZE_LED_PIN, GPIO.OUT)

def alarm_ausloesen(snooze_time=5):
    # Schalten Sie das Relais ein
    print('Alarm ausgelöst ', datetime.now())
    GPIO.output(SNOOZE_LED_PIN, GPIO.LOW)
    GPIO.output(RELAY_PIN, GPIO.HIGH)
    start_time = time.time()
    snoozed = False
    while time.time() - start_time < 15 * 60:
        # Überprüfen Sie, ob der Knopf gedrückt wurde
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            break
        # Überprüfen Sie, ob der Snooze-Knopf gedrückt wurde
        if GPIO.input(SNOOZE_BUTTON_PIN) == GPIO.LOW:
            snoozed = True
            print('Snooze ', datetime.now())
            break
        # Warten Sie 0,1 Sekunden, bevor Sie erneut überprüfen
        time.sleep(0.1)
    # Schalten Sie das Relais aus
    GPIO.output(RELAY_PIN, GPIO.LOW)
    # Wenn die Snooze-Funktion aktiviert wurde, wird die snooze_time-Wartezeit eingestellt,
    # dies kann durch Drücken den Knopf button_pin abgebrochen werden
    if snoozed:
        GPIO.output(SNOOZE_LED_PIN, GPIO.HIGH)
        start_time = time.time()
        while time.time() - start_time < snooze_time * 60:
            if GPIO.input(BUTTON_PIN) == GPIO.LOW:
                break
            time.sleep(0.1)
        alarm_ausloesen()
    GPIO.output(SNOOZE_LED_PIN, GPIO.LOW)

def naechste_weckzeit(weckzeiten):
    jetzt = datetime.now()
    naechste_weckzeit = None
    for weckzeit in weckzeiten:
        tage = weckzeit[0]
        stunden = weckzeit[1]
        minuten = weckzeit[2]
        aktiviert = weckzeit[3]
        if not aktiviert:
            continue
        for tag in tage:
            tage_diff = (tag - jetzt.weekday() - 1) % 7
            naechster_tag = jetzt + timedelta(days=tage_diff)
            weckzeit = naechster_tag.replace(hour=stunden, minute=minuten, second=0, microsecond=0)
            if weckzeit <= jetzt:
                weckzeit += timedelta(days=7)
            if naechste_weckzeit is None or weckzeit < naechste_weckzeit:
                naechste_weckzeit = weckzeit
    return naechste_weckzeit


def alarms_read():
    try:
        with open('/media/pi/16D3-BA21/clock/Wecker.txt', 'r') as datei:
            alarm_liste = ast.literal_eval(datei.read())
        return alarm_liste
    except Exception as e:
        print(f'Fehler beim Lesen der Weckzeiten: {e}')
        return []


if __name__ == '__main__':
    while True:
        # Lesen Sie die Liste der Weckzeiten aus der Datei
        weckzeiten = alarms_read()
        # Überprüfen Sie, ob es Zeit für einen Alarm ist
        naechste_zeit = naechste_weckzeit(weckzeiten)
        zeit_jetzt = datetime.now()
        # rechne zwei sekunden auf die aktuelle Zeit darauf
        zeit_jetzt = zeit_jetzt + timedelta(seconds=2)
        if naechste_zeit is not None and zeit_jetzt >= naechste_zeit:
            # Lösen Sie den Alarm aus
            alarm_ausloesen()
        if GPIO.input(SNOOZE_BUTTON_PIN) == GPIO.LOW and GPIO.input(BUTTON_PIN) == GPIO.LOW:
            time.sleep(3)
            print("manuelle Alarmauslösung", datetime.now())
            # Lösen Sie den Alarm aus
            alarm_ausloesen()
        # Warten Sie 1 Sekunde, bevor Sie erneut überprüfen
        time.sleep(1)
