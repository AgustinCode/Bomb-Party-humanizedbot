import subprocess

libraries=['pyautogui','pyperclip','keyboard']

for lib in libraries:
    subprocess.call(['pip','install',lib])

print("Libraries have been successfully installed")