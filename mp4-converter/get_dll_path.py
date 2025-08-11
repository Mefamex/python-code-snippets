import openH264_setup
dll = openH264_setup.find_openh264_dll_silent()
if dll: print(dll.absolute())
else: print("")
