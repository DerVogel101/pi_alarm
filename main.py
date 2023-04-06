import subprocess
import sys
from time import sleep
# führe die dateien lcd.py und alarm.py aus und gebe ihre ausgaben in der konsole aus
lcd_process = subprocess.Popen(["python3", 'lcd.py'], stdout=sys.stdout)
alarm_process = subprocess.Popen(["python3", 'alarm.py'], stdout=sys.stdout)
while True:
    try:
        sleep(2)  # Warte 2 Sekunde, um die CPU nicht unnötig zu belasten
        pass
    except:
        # Schließe die Unterprozesse, wenn das Hauptprogramm durch Strg-C abgebrochen wird
        lcd_process.terminate()
        alarm_process.terminate()
        break


