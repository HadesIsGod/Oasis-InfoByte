import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime

# Create the main window
window = tk.Tk()
window.title("BMI Calculator")

# Set window size and background color
window.geometry("500x300")
window.configure(bg="#f0f0f0")  # Light gray background color

# Create the input fields
weight_label = tk.Label(window, text="Weight (kg):", bg="#f0f0f0", pady=5)  # Match background color
weight_entry = tk.Entry(window)
height_label = tk.Label(window, text="Height (cm):", bg="#f0f0f0", pady=5)  # Match background color
height_entry = tk.Entry(window)

# Create the calculate button
calculate_button = tk.Button(window, text="Calculate BMI", bg="#007BFF", fg="white", padx=10, pady=5, bd=0)

# Create the output labels
bmi_label = tk.Label(window, text="BMI:", bg="#f0f0f0", pady=5)  # Match background color
category_label = tk.Label(window, text="Category:", bg="#f0f0f0", pady=5)  # Match background color

# Create the data storage
connection = sqlite3.connect("bmi_data.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS bmi_data (user_id INTEGER PRIMARY KEY AUTOINCREMENT, weight REAL, height REAL, bmi REAL, date TEXT)")

# Define the calculate BMI function
def calculate_bmi():
    weight = float(weight_entry.get())
    height = float(height_entry.get())
    bmi = weight / (height / 100) ** 2
    bmi_label.config(text="BMI: {:.2f}".format(bmi))

    category = determine_category(bmi)
    category_label.config(text="Category: " + category)

    # Get the current date
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Get the latest user_id
    cursor.execute("SELECT MAX(user_id) FROM bmi_data")
    latest_user_id = cursor.fetchone()[0]

    # Increment the latest user_id by 1
    if latest_user_id is None:
        user_id = 1
    else:
        user_id = latest_user_id + 1

    # Store the data in the database
    cursor.execute("INSERT INTO bmi_data (user_id, weight, height, bmi, date) VALUES (?, ?, ?, ?, ?)",
                   (user_id, weight, height, bmi, current_date))
    connection.commit()

def determine_category(bmi):
    if bmi < 16:
        return "Severely Underweight"
    elif 16 <= bmi <= 18.5:
        return "Underweight"
    elif 18.5 < bmi < 25:
        return "Healthy"
    elif 25 <= bmi < 30:
        return "Overweight"
    elif bmi >= 30:
        return "Obese"

# Define the view historical data function
def view_historical_data():
    # Create a new window
    historical_data_window = tk.Toplevel(window)  # Use Toplevel instead of Tk
    historical_data_window.title("Historical BMI Data")

    # Create a treeview to display the data
    tree = ttk.Treeview(historical_data_window)  # Use ttk.Treeview
    tree["columns"] = ("user_id", "date", "weight", "height", "bmi")
    tree.heading("#0", text="User ID")
    tree.heading("user_id", text="User ID")
    tree.heading("date", text="Date")
    tree.heading("weight", text="Weight (kg)")
    tree.heading("height", text="Height (cm)")
    tree.heading("bmi", text="BMI")

    # Insert the data into the treeview
    cursor.execute("SELECT * FROM bmi_data")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

    # Pack the treeview
    tree.pack()

# Define the analyze BMI trend function
def analyze_bmi_trend():
    # Get the BMI data
    cursor.execute("SELECT * FROM bmi_data")
    bmi_data = cursor.fetchall()

    # Extract dates and BMIs
    dates = [row[4] for row in bmi_data]
    bmis = [row[3] for row in bmi_data]

    # Plot the graph
    plt.plot(dates, bmis, marker='o')
    plt.xlabel('Date')
    plt.ylabel('BMI')
    plt.title('BMI Trend Analysis')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()  # Adjust layout to prevent labels from overlapping
    plt.show()

# Bind the calculate button to the calculate BMI function
calculate_button.config(command=calculate_bmi)

# Bind the view historical data button to the view historical data function
view_historical_data_button = tk.Button(window, text="View Historical Data", command=view_historical_data, bg="#28A745", fg="white", padx=10, pady=5, bd=0)

# Bind the analyze BMI trend button to the analyze BMI trend function
analyze_bmi_trend_button = tk.Button(window, text="Analyze BMI Trend", command=analyze_bmi_trend, bg="#DC3545", fg="white", padx=10, pady=5, bd=0)

# Pack the widgets with appropriate spacing
weight_label.pack()
weight_entry.pack()
height_label.pack()
height_entry.pack()
calculate_button.pack(pady=10)
bmi_label.pack()
category_label.pack()
view_historical_data_button.pack(pady=5)
analyze_bmi_trend_button.pack(pady=5)

# Run the main loop
window.mainloop()
