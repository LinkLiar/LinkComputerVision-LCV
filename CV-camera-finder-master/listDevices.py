from CameraFinder import GetDevices
import os
device_list = GetDevices()
print("OpenCV Index List:")
for i, device_name in enumerate(device_list):
    print(f"{i}: Device Name:{device_name}")
os.system("pause")
