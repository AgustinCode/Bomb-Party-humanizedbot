import time
import random
import pyperclip
import keyboard
import pyautogui
from ClassCords import ClassCords

# Humanized Bomb Party bot.
# You'll probably need to configure your coordinates, use get-rgb-coords.py to get them
# This is my first project so more functionalities can be added.

try:
    
    with open("wordlist.txt", "r") as file:
        words = file.read().splitlines()

except FileNotFoundError:
    print("You must add a word list.")

intervals = [0.007, 0.01, 0.0010, 0.002, 0.004, 0.002, 0.004, 0.007, 0.01, 0.002, 0.004, 0.007, 0.01, 0.0010, 0.02, 0.0015, 0.018, 0.1, 0.2, 0.1, 0.2]
writebox_x, writebox_y = 0, 0  # Writebox coords
syllabex, syllabey = 0, 0  # Syllabe coords
joinx, joiny = 0, 0  # Join button coords


def get_coords():
    #Function added in order to correctly store coordinates.
    global syllabex, syllabey
    global joinx, joiny
    global writebox_x, writebox_y

    print("Move your mouse to the syllabes and press F6")
    keyboard.wait("F6")
    syllabex, syllabey = ClassCords.return_cords()
    print("Now move your mouse to the 'Join' button and press F6 again")
    keyboard.wait("F6")
    joinx, joiny = ClassCords.return_cords()
    print("Last one! Move your mouse to the text box in the game then press F6")
    keyboard.wait("F6")
    writebox_x, writebox_y = ClassCords.return_cords()
    print(f"Syllabes: {syllabex, syllabey}")
    print(f"Join: {joinx, joiny}")
    print(f"Writebox: {writebox_x, writebox_y}\n")
    print("Done! Starting in 3 seconds")
    time.sleep(3)


def main():
    option = mode_selector()
    match option:
        case 1:
            print("Starting automatic mode in 3 seconds. Join a lobby!")
            time.sleep(3)
            print("\n\nRunning on automatic... Press F8 to stop (Whenever it's not your turn)")
            automatic()
        case 2:
            print("Starting manual mode in 3 seconds. Join a lobby!")
            time.sleep(3)
            print("\n\nRunning on manual... Press F6 when is your turn to type a word --- Press F8 to stop (Whenever it's not your turn)")
            manual()


def mode_selector():
    while True:
        print("""Select an option:
            
                1-Automatic
                2-Hotkey based
                """)
        try:
            op=int (input("1/2: "))
            if op in [1,2]:
                return op
            else:
                print("\nINVALID OPTION: Please select option 1 or 2.\n")
        except ValueError:
            print("\nInvalid Option: Only numbers allowed (1, 2)!\n")
        

def automatic():
    bot_is_on=True
    
    while bot_is_on:
        
        if autojoin(): #Checks if "join" button is on the screen returning true if so
            pyautogui.click(joinx,joiny) #If "join" button is on the screen, clicks it
        
        else:
            
            if turn():
                try:
                    silava = copysil_paste()
                    words_found = findWord(silava, words)
                    
                    # Probability of typing a long word or a short one
                    long_prob = random.randint(0, 100)
                    if long_prob <= 25:
                        toWrite = max(words_found, key=len)
                    if long_prob > 25:
                        toWrite = random.choice(words_found)

                    words.remove(toWrite)  # Prevents from writing the same words
                    pyautogui.moveTo(writebox_x, writebox_y)
                    pyautogui.click()
                    time.sleep(random.uniform(0.1, 0.4))
                    typewrite(toWrite, intervals)
                    time.sleep(0.0002)
                    pyautogui.press('enter')
                    time.sleep(0.3)
                except IndexError:
                    print("No words found")
            
            elif not turn():
                
                try:
                    #Tells if the user wants to exit
                    if keyboard.is_pressed("F8"):
                        bot_is_on = False
                except Exception as e:
                    print(f"Error: {e}")
                
                finally:
                    time.sleep(0.1) #Prevents multiple keyboard taps
                    continue

                
def manual():
    bot_is_on=True
    
    while bot_is_on:
        
            while turn():
                
                try: 
                       
                    if keyboard.is_pressed("alt"):
                        
                        silava = copysil_paste()
                        words_found = findWord(silava, words)
                        
                        # Probability of typing a long word or a short one
                        long_prob = random.randint(0, 100)
                        if long_prob <= 50:
                            toWrite = max(words_found, key=len)
                        if long_prob > 25:
                            toWrite = random.choice(words_found)

                        words.remove(toWrite)  # Prevents from writing the same words
                        pyautogui.moveTo(writebox_x, writebox_y)
                        pyautogui.click()
                        time.sleep(random.uniform(0.1, 0.4))
                        typewrite(toWrite, intervals)
                        time.sleep(0.0002)
                        pyautogui.press('enter')
                        time.sleep(0.3)
                        
                except IndexError:
                    
                    time.sleep(1)
                    print("No words found")
                
            while not turn():
                    
                try:
                    #Tells if the user wants to exit
                    if keyboard.is_pressed("F8"):
                        bot_is_on = False
                
                except Exception as e:
                    print(f"Error: {e}")
                
                finally:
                    time.sleep(0.1) #Prevents multiple keyboard taps
                    continue           

         
def autojoin():
    # Checks green color of "Join game" button, returns True if on screen
    target_color_turn = (38, 170, 54) #Join button color
    pixel_x, pixel_y = 572, 683 #Pixel shown at coords x,y
    return pyautogui.pixel(pixel_x, pixel_y) == target_color_turn


def turn():
    # Checks black color of write box, if true, means it's your turn. Similar to autojoin()
    target_color = (21, 19, 16)
    pixel_x, pixel_y = 823, 698

    return pyautogui.pixel(pixel_x, pixel_y) == target_color


def copysil_paste():
    # Copies the given syllable then returns it as pyperclip.paste
    pyautogui.moveTo(syllabex, syllabey)
    pyautogui.doubleClick()
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.01)
    silava = pyperclip.paste()
    return silava


def findWord(silava, words):
    # Simply find words containing syllable
    words_with_syllabe = [word for word in words if silava in word]
    return words_with_syllabe #Listed valid words


def typewrite(toWrite, intervals):
    # This function simulates human typing, it randomly makes type mistakes while writing
    for char in toWrite:
        random_char = random.choice('abcdefghijklmnopqrstuvwxyz')
        rand_prob = random.randint(0, 100)
        if rand_prob > 5:  # Works as probability, from 1% to 100%, tweak this as you want
            pyautogui.write(char)
            time.sleep(random.choice(intervals))
        else:
            pyautogui.write(random_char)
            time.sleep(random.uniform(0.01, 0.2))
            pyautogui.press('backspace')
            time.sleep(0.0005)
            pyautogui.write(char)


get_coords()


main()