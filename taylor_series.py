import matplotlib.pyplot as plt
import numpy as np
from colorama import init, Fore, Style
import os
import platform

# Initialize colorama
init(autoreset=True)

def clear_console():
    if platform.system() == "Windows":
        os.system('cls')  # Use 'cls' for Windows systems
    else:
        os.system('clear')  # Use 'clear' for Unix-based systems (Linux, macOS)

# Clear the console at the start of the program
clear_console()

# Factorial function to compute n!
def factorial(n):
    """Returns the factorial of a given number n."""
    if n == 0:
        return 1
    fact = 1
    for i in range(2, 1 + n):
        fact *= i
    return fact

# Taylor series for different functions
def cos_taylor(x, terms):
    res = 0
    sig = 1
    for n in range(terms):
        res += (sig * x**(2*n)) / factorial(2*n)
        sig *= -1
    return res

def sin_taylor(x, terms):
    res = 0
    sig = 1
    for n in range(terms):
        res += (sig * x**(2*n + 1)) / factorial(2*n + 1)
        sig *= -1
    return res

def sinh_taylor(x, terms):
    res = 0
    for n in range(terms):
        res += (x**(2*n + 1)) / factorial(2*n + 1)
    return res

def cosh_taylor(x, terms):
    res = 0
    for n in range(terms):
        res += (x**(2*n)) / factorial(2*n)
    return res

def exp_taylor(x, terms):
    res = 0
    for n in range(terms):
        res += x**n / factorial(n)
    return res

def ln_taylor(x, terms):
    # This Taylor series is valid for ln(1 + x) where |x| < 1
    res = 0
    for n in range(1, terms + 1):
        res += ((-1)**(n+1)) * (x**n) / n
    return res

def arcsin_taylor(x, terms):
    # This Taylor series is valid for |x| <= 1
    res = 0
    for n in range(terms):
        res += (factorial(2*n) / (4**n * factorial(n)**2 * (2*n + 1))) * x**(2*n + 1)
    return res

def arccos_taylor(x, terms):
    # Taylor series for arccos can be calculated as pi/2 - arcsin
    return (np.pi / 2) - arcsin_taylor(x, terms)

# Title of the simulation displayed in a decorative box
title = "Mathematical Function Approximation using Taylor Series"
box_width = 60
padding = (box_width - len(title)) // 2

# Print the title in a decorative box
print(f"{Fore.LIGHTCYAN_EX}{Style.BRIGHT}╔{'═'*box_width}╗")
print(f"{Fore.LIGHTCYAN_EX}{Style.BRIGHT}║{' '*padding}{Fore.YELLOW}{title}{' '*padding}{Fore.LIGHTCYAN_EX}║")
print(f"{Fore.LIGHTCYAN_EX}{Style.BRIGHT}╚{'═'*box_width}╝\n")
print(Fore.WHITE + "This tool will help you visualize how the Taylor series approximation improves for various functions.\n")
print()

# User selects the function to approximate
functions = {
    1: ("Cosine", cos_taylor, (-1.5, 1.5)),
    2: ("Sine", sin_taylor, (-1.5, 1.5)),
    3: ("Hyperbolic Sine (sinh)", sinh_taylor, (-100, 100)),
    4: ("Hyperbolic Cosine (cosh)", cosh_taylor, (0, 100)),
    5: ("Exponential (exp)", exp_taylor, (0, 100)),
    6: ("Natural Logarithm (ln(1 + x))", ln_taylor, (-2, 1)),
    7: ("Arcsine (arcsin)", arcsin_taylor, (-1.5, 1.5)),
    8: ("Arccosine (arccos)", arccos_taylor, (0, np.pi))
}

while True:
    try:
        print(Fore.YELLOW + "Please choose which function to approximate:")
        for key, (name, _, _) in functions.items():
            print(Fore.CYAN + f"{key}: {name}")
        choice = int(input(Fore.CYAN + ">> "))
        if choice in functions:
            function_name, taylor_approximation, y_limits = functions[choice]
            break
        else:
            print(Fore.RED + "Error: Please choose a valid option.")
    except ValueError:
        print(Fore.RED + "Error: Please enter a valid integer.")

# User selects the number of terms for the Taylor series
while True:
    try:
        print(Fore.YELLOW + "Please enter the maximum number of terms for the Taylor series (positive integer): ")
        max_terms = int(input(Fore.CYAN + ">> "))
        print(Fore.YELLOW + "Please enter the maximum number of periods or range of the signal (positive integer): ")
        max_periods_of_pi = int(input(Fore.CYAN + ">> "))
        if max_terms > 0 and max_periods_of_pi > 0:
            break
        else:
            print(Fore.RED + "Error: Please enter a number greater than 0.")
    except ValueError:
        print(Fore.RED + "Error: Please enter a valid integer.")

# Create x values for the plot over a wide range
x_vals = np.linspace(-max_periods_of_pi * np.pi, max_periods_of_pi * np.pi, 400)

# Compute the real function values using numpy
if function_name == "Cosine":
    real_function = np.cos(x_vals)
elif function_name == "Sine":
    real_function = np.sin(x_vals)
elif function_name == "Hyperbolic Sine (sinh)":
    real_function = np.sinh(x_vals)
elif function_name == "Hyperbolic Cosine (cosh)":
    real_function = np.cosh(x_vals)
elif function_name == "Exponential (exp)":
    real_function = np.exp(x_vals)
elif function_name == "Natural Logarithm (ln(1 + x))":
    real_function = np.log(1 + x_vals)
elif function_name == "Arcsine (arcsin)":
    real_function = np.arcsin(x_vals)
elif function_name == "Arccosine (arccos)":
    real_function = np.arccos(x_vals)

# Configure the plot for live updating
plt.ion()  # Enable interactive mode for live updates
fig, ax = plt.subplots()
ax.plot(x_vals, real_function, label=f"math.{function_name.lower()}(x)", color="blue")  # Plot the real function

# Iterate and plot the Taylor series approximation for increasing terms
for terms in range(1, max_terms + 1):
    # Compute the Taylor series approximation for the current number of terms
    approx = [taylor_approximation(x, terms) for x in x_vals]
    
    # Clear previous plot lines before updating with new approximation
    ax.clear()
    
    # Plot the real function again
    ax.plot(x_vals, real_function, label=f"math.{function_name.lower()}(x)", color="blue")
    
    # Plot the current Taylor series approximation
    ax.plot(x_vals, approx, label=f"Taylor Series with {terms} term{'s' if terms > 1 else ''}", color="red", linestyle="--")
    
    # Set labels, title, and grid
    ax.set_title(f"{function_name} Approximation with Taylor Series ({terms} terms)")
    ax.set_xlabel("x")
    ax.set_ylabel(f"{function_name.lower()}(x)")
    ax.legend()
    ax.set_ylim(y_limits)  # Adjust based on the function range
    ax.grid(True)
    
    # Pause to visualize the update
    plt.pause(1)

# Turn off interactive mode and show the final plot
plt.ioff()
plt.show()

# Final message in color
print(Fore.CYAN + Style.BRIGHT + "Visualization complete!")
print(Fore.GREEN + f"Thank you for using the Taylor Series Approximation tool for {function_name}.")
