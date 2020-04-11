import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify, GdkPixbuf
import time


class BatteryNotifier:
    def __init__(self):
        self.battery_percent = self.getBatteryPercent()
        self.power_plugged = self.getPowerPlugged()
        self.createNotification()
        
    def getBatteryPercent(self):
        """ Reads battery information from the system files """
        with open("/sys/class/power_supply/BAT0/charge_full") as f:
            charge_full = int(f.read().replace("\n", "")) # The battery's full potential 
        with open("/sys/class/power_supply/BAT0/charge_now") as f:
            charge_now = int(f.read().replace("\n", "")) # The battery's charge right now    
        battery_percent = int(round((charge_now/charge_full)*100))
        return battery_percent

    def getPowerPlugged(self):
        """ Reads battery information from the system files """
        with open("/sys/class/power_supply/BAT0/status") as f:
            status = f.read().replace("\n", "") # Battery status: Discharging or Charging
        if status == "Discharging":
            power_plugged = False
        else:
            power_plugged = True
        return power_plugged

    def createNotification(self):
        """ Creats notification based on the obtained values """        
        if self.power_plugged == True and self.battery_percent >= 80:
            Notify.init("Charger Notifier")
            notification = Notify.Notification.new(
                "BATTERY",
                "Battery level is over 80%! Please unplug the charger.",
                "dialog-information"
            )
            notification.show()
        elif self.power_plugged == False and self.battery_percent <= 40:
            Notify.init("Charger Notifier")
            notification = Notify.Notification.new(
                "BATTERY",
                "Battery level is less than 40%! Please plug in the charger.",
                "dialog-information"
            )
            notification.show()
       

while True:
    if __name__ == "__main__":
        battery_notifier = BatteryNotifier()
        time.sleep(20)
