import os


def install(module):
    if module == "cvzone":
        os.system(f'py -m pip install cvzone==1.4.1 --quiet') if os.name == 'nt' else os.system(f'pip3 install cvzone==1.4.1 --quiet')
    else:
        os.system(f'py -m pip install {module}') if os.name == 'nt' else os.system(f'pip3 install {module}')
    print(f"    [>] Installing {module}")


print("    Welcome to the setup! \n")

install("opencv-python")
install("cvzone")
install("numpy")
install("pycaw")

print("    What do you want to start?")
print("     [1] > VolumeHandControl")

value = input("> ")

if value.isdigit():
    if value == "1":
        filepath = input("    Path for volumeHandControl.py: ")
        os.startfile(filepath)
