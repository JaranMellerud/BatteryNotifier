import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify, GdkPixbuf
import time

class Notifier:
    def __init__(self):

        # reading battery information from the system files
        with open("/sys/class/power_supply/BAT0/status") as f:
            status = f.read().replace("\n", "")
        with open("/sys/class/power_supply/BAT0/charge_full") as f:
            charge_full = int(f.read().replace("\n", ""))
        with open("/sys/class/power_supply/BAT0/charge_now") as f:
            charge_now = int(f.read().replace("\n", ""))

        if status == "Discharging":
            power_plugged = False
        else:
            power_plugged = True
        battery_percent = int(round((charge_now / charge_full) * 100))
        
        # creating notificatison based on the values
        if power_plugged == True and battery_percent >= 80:
            Notify.init("Charger Notifier")
            notification = Notify.Notification.new(
                "BATTERY",
                "Battery level is over 80%! Please unplug the charger.",
                "dialog-information"
            )
            notification.show()
        elif power_plugged == False and battery_percent <= 70:
            Notify.init("Charger Notifier")
            notification = Notify.Notification.new(
                "BATTERY",
                "Battery level is less than 40%! Please plug in the charger.",
                "dialog-information"
            )
            notification.show()
       
        time.sleep(600)

while True:
    charger_notifier = Notifier()
