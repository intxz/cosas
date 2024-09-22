import random
import time
from colorama import init, Fore, Style
import os
import platform
import re

# Initialize colorama for colored console output
init(autoreset=True)

# Function to clear the console screen depending on the operating system
def clear_console():
    if platform.system() == "Windows":
        os.system('cls')  # Use 'cls' for Windows systems
    else:
        os.system('clear')  # Use 'clear' for Unix-based systems (Linux, macOS)

# Clear the console at the start of the program
clear_console()

# Title of the simulation displayed in a decorative box
title = "Infinite Monkey Theorem Simulation"
box_width = 52  # Define the width of the box
padding = (box_width - len(title)) // 2  # Calculate padding to center the title

# Print the title in a decorative box
print(f"{Fore.LIGHTCYAN_EX}{Style.BRIGHT}╔{'═'*box_width}╗")
print(f"{Fore.LIGHTCYAN_EX}{Style.BRIGHT}║{' '*padding}{Fore.YELLOW}{title}{' '*padding}{Fore.LIGHTCYAN_EX}║")
print(f"{Fore.LIGHTCYAN_EX}{Style.BRIGHT}╚{'═'*box_width}╝\n")

# Print the description of the Infinite Monkey Theorem
print(f"{Fore.LIGHTWHITE_EX}{Style.BRIGHT}Infinite Monkey Theorem Description:")
print(f"{Fore.WHITE}The Infinite Monkey Theorem suggests that a monkey randomly typing on a keyboard for an infinite")
print(f"amount of time will eventually produce any given text, such as the works of Shakespeare. The theorem")
print(f"is often used to explain the concept of probability over long periods of time.")
print(f"This simulation attempts to generate a random word or phrase by selecting characters from a limited pool.\n")

# The character pool for random generation (English letters, apostrophes, and spaces)
character_pool = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + ["'", " "]

# Regular expression to validate that the input contains only valid characters
valid_characters_pattern = re.compile(r"^[A-Z' ]+$")

# Function to check if the user's input is valid (only contains allowed characters)
def is_valid_input(user_input):
    return bool(valid_characters_pattern.match(user_input))

# Loop to prompt the user to input a valid word or phrase
while True:
    print(Fore.YELLOW + "Please enter a word or phrase (English only): ")
    word1 = input(Fore.CYAN + ">> ").upper()  # Convert input to uppercase
    if is_valid_input(word1):
        break  # Exit the loop if input is valid
    else:
        print(f"{Fore.RED}Error: Please enter a word or phrase using only English letters (A-Z), apostrophes, or spaces.")

# Clear the console after the user enters a valid word/phrase
clear_console()

# Initialize variables for tracking the simulation
word2 = ['_'] * len(word1)  # Initialize the generated word as underscores (same length as target word)
x = 0  # Count the number of attempts
start_time = time.time()  # Record the starting time of the simulation
probability = 1 / 28**len(word1)  # Calculate the probability of randomly generating the target word

# Function to generate a random word of the same length as the target word
def random_word(length):
    character_pool = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + ["'", " "]  # Allowed characters
    return ''.join(random.choice(character_pool) for _ in range(length))  # Return a random word of given length

# Function to calculate the elapsed time since the start of the program
def calc_time(start_time):
    end_time = time.time()  # Get the current time
    elapsed_time = end_time - start_time  # Calculate time difference in seconds

    years = int(elapsed_time // (365 * 24 * 3600))  # Calculate years
    elapsed_time = elapsed_time % (365 * 24 * 3600)  # Remaining time after calculating years
    days = int(elapsed_time // (24 * 3600))  # Calculate days
    elapsed_time = elapsed_time % (24 * 3600)  # Remaining time after calculating days
    hours = int(elapsed_time // 3600)  # Calculate hours
    elapsed_time %= 3600  # Remaining time after calculating hours
    minutes = int(elapsed_time // 60)  # Calculate minutes
    seconds = int(elapsed_time % 60)  # Calculate seconds

    return years, days, hours, minutes, seconds, elapsed_time

# Print the title again after clearing the console
print(f"{Fore.LIGHTCYAN_EX}{Style.BRIGHT}╔{'═'*box_width}╗")
print(f"{Fore.LIGHTCYAN_EX}{Style.BRIGHT}║{' '*padding}{Fore.YELLOW}{title}{' '*padding}{Fore.LIGHTCYAN_EX}║")
print(f"{Fore.LIGHTCYAN_EX}{Style.BRIGHT}╚{'═'*box_width}╝")

# Display the calculated probability of generating the target word randomly
print(f"{Fore.CYAN}The probability of generating '{Fore.GREEN}{word1}{Fore.CYAN}' randomly is "
      f"{Fore.YELLOW}{probability:.10f}")

# Main loop to generate random words until a match is found
while True:
    x += 1  # Increment the number of attempts
    word2 = random_word(len(word1))  # Generate a random word of the same length as the target word
    years, days, hours, minutes, seconds, elapsed_time = calc_time(start_time)  # Calculate the elapsed time

    # Calculate requests per second by dividing the number of attempts by the elapsed time
    if elapsed_time > 0:
        requests_per_second = x / elapsed_time
    else:
        requests_per_second = 0

    # Print the current progress, including attempts, target word, generated word, and time elapsed
    print(f"{Fore.CYAN}| Attempts: {Fore.YELLOW}{x:,} {Fore.CYAN}| " 
          f"Target Word or Phrase: {Fore.GREEN}{word1} {Fore.CYAN}| "
          f"Generated Word or Phrase: {Fore.MAGENTA}{word2} {Fore.CYAN}| "
          f"Time Elapsed: {Fore.RED}{years}y {days}d {hours}h {minutes}m {seconds}s {Fore.CYAN}| "
          f"Attempts per second: {Fore.BLUE}{requests_per_second:.2f}", end="\r")

    # If the generated word matches the target word, print the result, attempts, and total time taken
    if word2 == word1:
        print(f"\n{Fore.GREEN}Match found! {Fore.CYAN}Attempts: {Fore.YELLOW}{x:,}, "
              f"{Fore.CYAN}Target Word or Phrase: {Fore.GREEN}{word1}, {Fore.CYAN}Generated Word or Phrase: {Fore.MAGENTA}{word2}")
        print(f"{Fore.CYAN}Total Time Taken: {Fore.RED}{years} years, {days} days, {hours} hours, {minutes} minutes, {seconds} seconds")
        break
