import requests
import tkinter as tk
from tkinter import messagebox
API_KEY = "8eaab9520bac6ff86b7a3c59170d2e73"

def get_weather():
    city = city_entry.get()

    if not city:
        messagebox.showwarning("Missing Input", "Please enter a city name.")
        return

    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            weather = f"""
City: {data['name']}, {data['sys']['country']}
Temperature: {data['main']['temp']}°C
Condition: {data['weather'][0]['description'].capitalize()}
Humidity: {data['main']['humidity']}%
Wind Speed: {data['wind']['speed']} m/s
"""
            result_label.config(text=weather)
        else:
            result_label.config(text="Error: " + data.get("message", "Unable to fetch data"))
    except Exception as e:
        result_label.config(text="Error: " + str(e))


# GUI Setup
app = tk.Tk()
app.title("Weather Forecasting System")
app.geometry("400x300")
app.resizable(False, False)

tk.Label(app, text="Enter City Name:").pack(pady=5)
city_entry = tk.Entry(app, width=30)
city_entry.pack(pady=5)

tk.Button(app, text="Get Weather", command=get_weather).pack(pady=10)

result_label = tk.Label(app, text="", justify="left", font=("Courier", 10))
result_label.pack(pady=10)

app.mainloop()

tk.Button(app, text="Get Weather", command=get_weather).pack(pady=10)

result_label = tk.Label(app, text="", justify="left", font=("Courier", 10))
result_label.pack(pady=10)

app.mainloop()
