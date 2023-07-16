from DeviceManager import DeviceMonitor
import time

my_Monitor = DeviceMonitor(
    lambda device_id: print(f"device is {device_id} in."),
    lambda device_id: print(f"device is {device_id} out."))
my_Monitor.start()

print("Let's go.")

for i in range(5):
    pass
    time.sleep(1)


while True:
    pass
