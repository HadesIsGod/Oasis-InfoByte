import tkinter as tk
from tkinter import messagebox, font
import random
import string
import pyperclip


def generate_password(length, use_letters=True, use_numbers=True, use_symbols=True):
    characters = ''

    if use_letters:
        characters += string.ascii_letters
    if use_numbers:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    if not characters:
        messagebox.showwarning("Error", "Please select at least one character type.")
        return None

    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def generate_password_and_update_label():
    try:
        length = int(length_entry.get())
        use_letters = letters_var.get()
        use_numbers = numbers_var.get()
        use_symbols = symbols_var.get()

        password = generate_password(length, use_letters, use_numbers, use_symbols)

        if password:
            password_var.set(password)
    except ValueError:
        messagebox.showerror("Error", "Invalid input for password length.")


def copy_to_clipboard():
    password = password_var.get()
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Success", "Password copied to clipboard!")


# Create main window
window = tk.Tk()
window.title("Password Generator")

# Set window size
window.geometry("1100x800")  # Set a larger window size

# Title label
title_label = tk.Label(window, text="Random Password Generator", font=("Helvetica", 16, "bold"))
title_label.pack(pady=(20, 10))

# Password Length
length_label = tk.Label(window, text="Password Length:", font=("Helvetica", 12))
length_label.pack()

length_entry = tk.Entry(window, font=("Helvetica", 12), width=10)
length_entry.pack(pady=5)

# Character Type Checkboxes
letters_var = tk.BooleanVar(value=True)
letters_check = tk.Checkbutton(window, text="Include Letters", font=("Helvetica", 12), variable=letters_var)
letters_check.pack(anchor=tk.W)

numbers_var = tk.BooleanVar(value=True)
numbers_check = tk.Checkbutton(window, text="Include Numbers", font=("Helvetica", 12), variable=numbers_var)
numbers_check.pack(anchor=tk.W)

symbols_var = tk.BooleanVar(value=True)
symbols_check = tk.Checkbutton(window, text="Include Symbols", font=("Helvetica", 12), variable=symbols_var)
symbols_check.pack(anchor=tk.W)

# Generate Button
generate_button = tk.Button(window, text="Generate Password", font=("Helvetica", 12),
                            command=generate_password_and_update_label)
generate_button.pack(pady=10)

# Generated Password Display
password_var = tk.StringVar()
password_label = tk.Label(window, text="Generated Password:", font=("Helvetica", 12))
password_label.pack(pady=(10, 5))

password_display = tk.Entry(window, textvariable=password_var, font=("Helvetica", 12), state="readonly", width=30)
password_display.pack(pady=5)

# Copy Button
copy_button = tk.Button(window, text="Copy to Clipboard", font=("Helvetica", 12), command=copy_to_clipboard)
copy_button.pack(pady=10)

# Start the GUI main loop
window.mainloop()
