from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import time

# Ask the user for the number of messages, the message itself, and the contact/group
x = int(input("How many times do you want to send the message?: "))
message = input("Enter the message you want to send: ")
contact = input("Enter the name of the contact or group: ")

# Prompt user to scan the QR code
print('Please scan the QR code. If it does not work, close the script and ensure that you logged out from previous sessions.')

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()

# Open WhatsApp Web
driver.get("https://web.whatsapp.com/")

# Try to load cookies from a file to avoid scanning the QR code again
try:
    cookies = pickle.load(open("whatsapp_cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()  # Refresh to apply the cookies and log in automatically
except FileNotFoundError:
    # If no cookies are found, the user will need to scan the QR code manually
    print("No saved cookies found. You will need to scan the QR code manually.")
    time.sleep(15)  # Give the user 15 seconds to scan the QR code

# Initialize WebDriverWait to wait for elements to load
wait = WebDriverWait(driver, 30)

# Locate the search box to search for the contact/group
search_box = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')))
search_box.send_keys(contact)  # Type the contact or group name
search_box.send_keys(Keys.ENTER)  # Press Enter to open the chat
time.sleep(2)  # Wait for the chat to load

# Locate the message input box
input_box = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')))

# Loop to send the message `x` times
for _ in range(x):
    input_box.send_keys(message)  # Type the message
    input_box.send_keys(Keys.ENTER)  # Press Enter to send the message
    time.sleep(0.1)  # Small delay between messages

# Close the browser after sending the messages
driver.quit()
