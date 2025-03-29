import requests
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from twilio.rest import Client

# Mock weather data for demonstration purposes
def get_weather_data(latitude, longitude):
    # In a real-world scenario, this function would fetch data from a weather API.
    data = {
        'temperature': [28, 30, 32, 29, 31],
        'humidity': [45, 40, 38, 42, 37],
        'rainfall': [0, 0, 0, 2, 0], #in mm
        'soil_moisture': [35, 32, 30, 33, 29], #in %
        'evapotranspiration': [5, 6, 7, 5, 6] #in mm/day
    }
    return pd.DataFrame(data)

# Drought prediction model
def train_drought_model():
    """Train a simple drought prediction model"""
    # In a real-world scenario, this function would train a model on historical data.
    x = [[30, 50, 10, 40, 5],
         [35, 30, 0, 30, 8],
         [28, 60, 15, 45, 4]]
    y = [0, 1, 0] # 1: Drought

    model = RandomForestClassifier()
    model.fit(x, y)
    return model

# Irrigation recommendation
def recommend_irrigation(prediction, soil_moisture, forecast):
    """Generate irrigation recommendations"""
    if prediction == 1: # Drought predicted
        if soil_moisture < 30:
            return "Critical: Irrigate immediately with 20mm water."
        else:
            return "Warning: Irrigate with 10mm water tomorrow morning."
    else:
        if soil_moisture < 35:
            return "Advisory: Light irrigation recommended."
        else:
            return "No irrigation needed."
        
# Send SMS alert
def send_sms_alert(message, phone_number):
    """Send SMS alert using Twilio"""
    # In a real-world scenario, you would use your Twilio credentials here.
    print(f"SMS sent to {phone_number}: {message}")
    # Example real implementation:
    # account_sid = 'your_account_sid'
    # auth_token = 'your_auth_token'
    # client = Client(account_sid, auth_token)
    # message = client.messages.create(
    #     body=message,
    #     from_='+1234567890',  # Your Twilio number
    #     to=phone_number
    # )

# Main function to run the AgriAlert system
def main():
    print("AgriAlert - Drought Prediction and Irrigation Optimization")

    # Get user input
    latitude = float(input("Enter your farm latitude: "))
    longitude = float(input("Enter your farm longitude: "))
    phone_number = input("Enter your phone number for alerts: ")

    # Fetch weather data
    weather_data = get_weather_data(latitude, longitude)
    latest_data = weather_data.iloc[-1].values

    # Make prediction
    model = train_drought_model()
    prediction = model.predict([latest_data])[0]

    # Generate irrigation recommendation
    soil_moisture = latest_data[3]  # Assuming soil moisture is the 4th feature
    recommendation = recommend_irrigation(prediction, soil_moisture, weather_data)

    # Send SMS alert
    alert_message = f"AgriAlert: {'Drought likely' if prediction else 'No drought expected'}. {recommendation}"
    print("\n" + alert_message)
    send_sms_alert(alert_message, phone_number)

    # Show 5-day weather forecast
    print("\n5-Day Weather Forecast:")
    print(weather_data)

if __name__ == "__main__":
    main()

    