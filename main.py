# wie installiere ich lcddriver?
#   sudo pip3 install lcddriver
import lcddriver
import datetime
import time

def alarm():
    # Setze die Uhrzeiten für die Alarme
    alarm_times = [datetime.time(hour=11), datetime.time(hour=12)]

    # Setze die Wochentage für die Alarme (Montag = 0, Sonntag = 6)
    alarm_days = [0, 1, 2, 3, 4] # Montag bis Freitag

    while True:
        # Überprüfe, ob heute ein Alarm-Tag ist
        if datetime.datetime.now().weekday() in alarm_days:
            # Warte bis zum nächsten Alarm
            now = datetime.datetime.now().time()
            next_alarm_time = min(alarm_time for alarm_time in alarm_times if alarm_time > now)
            if now >= next_alarm_time:
                break
            time.sleep(1)

            # Führe eine Aktion aus, wenn der Alarm ausgelöst wird
            print("Alarm ausgelöst!")

        # Warte bis zum nächsten Tag
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        tomorrow = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
        time.sleep((tomorrow - datetime.datetime.now()).total_seconds())


if __name__ == "__main__":
    alarm()

