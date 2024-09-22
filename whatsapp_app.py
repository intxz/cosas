import pyautogui
import time
import pyperclip
import keyboard

# Prompt user for message details
x = int(input("How many times do you want to send the message?: "))
message = input("Enter the message you want to send: ")
pyperclip.copy(message)
contact = input("Enter the name of the contact or group: ")
print('Open WhatsApp Desktop or Web in 5 seconds. Do NOT switch windows.')

time.sleep(5)

print("If you want to stop the process, press 'q'.")

# Start the search for the contact
pyautogui.hotkey('ctrl', 'f')  
time.sleep(0.5)
pyautogui.hotkey('ctrl', 'a')  
time.sleep(0.5)
pyautogui.hotkey('backspace')  
time.sleep(0.5)
pyautogui.write(contact) 
time.sleep(0.5)
pyautogui.press('down')  
time.sleep(0.5)
pyautogui.press('enter')

time.sleep(2)

# Loop to send the message repeatedly
for _ in range(x):
    # Check for 'q' key to stop the process
    if keyboard.is_pressed('q'):
        print("\nProcess stopped by user.")
        break

    # Paste the message and press enter
    pyautogui.hotkey('ctrl', 'v')  
    pyautogui.press('enter') 
    print(f'Message {_ + 1} of {x} sent', end='\r')
    time.sleep(2)
