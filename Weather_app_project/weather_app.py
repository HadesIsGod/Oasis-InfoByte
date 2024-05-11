from PIL import Image, ImageTk
import tkinter as tk
import requests
from tkinter import messagebox  # Import messagebox for displaying error messages
import ttkbootstrap
import io



def get_weather(city):
    API_key = "5e32173b9fe98fd8fcf518c9a63b7c90"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    res = requests.get(url)

    if res.status_code == 404:
        messagebox.showerror("Error", "City Not Found")
        return None
    weather = res.json()
    icon_id = weather['weather'][0]['icon']
    temperature = weather['main']['temp']-273.15
    description = weather['weather'][0]['description']
    city = weather['name']
    country = weather['sys']['country']

    icon_url = f"http://openweathermap.org/img/wn/{icon_id}10d@2x.png"
    return (icon_url, temperature,  description, city, country)



def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return

    icon_url, temperature, description, city_name, country = result
    location_label.config(text=f"{city_name}, {country}")

    try:
        # Fetch the image data from the URL
        response = requests.get(icon_url, stream=True)
        response.raise_for_status()  # Raise an error for bad response status

        # Create an image object from the response content
        image_data = response.content
        image = Image.open(io.BytesIO(image_data))
        icon = ImageTk.PhotoImage(image)

        # Update the icon label with the loaded image
        icon_label.config(image=icon)
        icon_label.image = icon

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch image: {e}")

    # Update temperature and description labels
    temperature_label.config(text=f"Temperature: {temperature:.2f}°C")
    description_label.config(text=f"Description: {description}")


root = ttkbootstrap.Window(themename="morph")
root.title("Weather App")
root.geometry("400x400")

city_entry = ttkbootstrap.Entry(root, font="Helvetica, 18")
city_entry.pack(pady=10)

search_button = ttkbootstrap.Button(root, text="Search", command=search, bootstyle="warning")
search_button.pack(pady=10)

location_label = tk.Label(root, font="Helvetica 25")
location_label.pack(pady=20)

icon_label = tk.Label(root)
icon_label.pack()

temperature_label = tk.Label(root, font="Helvetica 14")
temperature_label.pack()

description_label = tk.Label(root, font="Helvetica 14")
description_label.pack()

root.mainloop()
