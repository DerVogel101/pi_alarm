from time import sleep, perf_counter
from datetime import datetime, timedelta
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import ast
import locale

locale.setlocale(locale.LC_TIME, 'de_DE.utf8')

# Modify this if you have a different sized character LCD
lcd_columns = 16
lcd_rows = 2


lcd_rs = digitalio.DigitalInOut(board.D22)
lcd_en = digitalio.DigitalInOut(board.D17)
lcd_d4 = digitalio.DigitalInOut(board.D25)
lcd_d5 = digitalio.DigitalInOut(board.D24)
lcd_d6 = digitalio.DigitalInOut(board.D23)
lcd_d7 = digitalio.DigitalInOut(board.D18)


# Initialise the lcd class
lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)


def alarms_read():
    # read alarms from file
    # return list of alarms
    try:
        with open('/media/pi/16D3-BA21/clock/Wecker.txt', 'r') as datei:
            alarm_liste = ast.literal_eval(datei.read())
        return alarm_liste
    except Exception as e:
        print(f'Fehler beim Lesen der Weckzeiten: {e}')
        return []


def next_alarm():
    # get next alarm from list
    # return next alarm
    weckzeiten = alarms_read()
    jetzt = datetime.now()
    naechste_zeit = None
    for weckzeit in weckzeiten:
        tage = weckzeit[0]
        stunden = weckzeit[1]
        minuten = weckzeit[2]
        aktiviert = weckzeit[3]
        if not aktiviert:
            continue
        for tag in tage:
            naechster_tag = jetzt + timedelta(days=(int(tag - 1) - jetzt.weekday()) % 7)
            weckzeit = naechster_tag.replace(hour=int(stunden), minute=int(minuten), second=0)
            if weckzeit <= jetzt:
                weckzeit += timedelta(days=7)
            if naechste_zeit is None or weckzeit < naechste_zeit:
                naechste_zeit = weckzeit
    return naechste_zeit


def wecker_out():
    global nachster_wecker
    next_alarm_time = next_alarm()
    if next_alarm_time is None:
        nachster_wecker = False
    else:
        tag = next_alarm_time.strftime('%a')
        zeit = next_alarm_time.strftime('%H:%M')
        nachster_wecker = f'{tag:>4} {zeit}'

# wipe LCD screen before we start
lcd.clear()
wecker_out()

timer = perf_counter()

while True:
    # check for new alarms, at a slower rate than updating the clock
    if perf_counter() - timer >= 30:
        wecker_out()
        timer = perf_counter()

    # date and time
    lcd_line_1 = datetime.now().strftime('%b %d  %H:%M:%S\n')

    # next alarm
    if nachster_wecker is False:
        lcd_line_2 = f'{"kein Wecker":^16}'
    else:
        lcd_line_2 = "Alarm " + nachster_wecker

    # combine both lines into one update to the display
    lcd.message = lcd_line_1 + lcd_line_2

    sleep(1)