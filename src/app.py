import os.path
import streamlit as st
import pandas as pd
import requests
import numpy as np
import time
from datetime import datetime
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.preprocessing import LabelEncoder
import plotly.graph_objects as go
import plotly.express as px
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

# Weather API URL
from api_key import api_key

base_url = "https://api.weatherapi.com/v1/current.json"

# CSV file path
csv_file = "data.csv"

# Set default city
default_city = "Moscow"

# Delta time threshold in seconds
delta_t = 1

# Function to fetch current weather data from weather API
def fetch_weather_data(city=default_city):
    params = {
        "key": api_key,
        "q": city,
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    return data

# Function to check if enough time has elapsed for a new entry
def check_delta_time(previous_time):
    current_time = time.time()
    return (current_time - previous_time) >= delta_t

# Function to add a new entry to the CSV file
def add_entry(mood, temperature, condition, humidity, wind_speed):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {
        "Time": current_time,
        "Mood": mood,
        "Temperature": temperature,
        "Condition": condition,
        "Humidity": humidity,
        "Wind Speed": wind_speed,
    }
    df = pd.DataFrame([entry])
    if os.path.isfile(csv_file):
        df.to_csv(csv_file, mode="a", header=False, index=False)
    else:
        df.to_csv(csv_file, index=False)

# Function to delete the last entry from the CSV file
def delete_last_entry():
    if os.path.isfile(csv_file):
        df = pd.read_csv(csv_file)
        if len(df) > 0:
            df = df[:-1]  # Remove last row
            df.to_csv(csv_file, index=False)

# Function to display the current weather
def display_current_weather(city=default_city):
    st.subheader("Current Weather")
    data = fetch_weather_data(city)
    temperature = data["current"]["temp_c"]
    condition = data["current"]["condition"]["text"]
    humidity = data["current"]["humidity"]
    wind_speed = data["current"]["wind_kph"]

    st.write(f"Temperature: {temperature}°C")
    st.write(f"Condition: {condition}")
    st.write(f"Humidity: {humidity}%")
    st.write(f"Wind Speed: {wind_speed} kph")

# Function to display the previous entries table
def display_previous_entries():
    st.subheader("My Entries")
    if os.path.isfile(csv_file):
        df = pd.read_csv(csv_file)
        df["Temperature"] = df["Temperature"].round(
            0).astype(int).astype(str) + "°C"
        df["Humidity"] = df["Humidity"].astype(int).astype(str) + "%"
        df["Wind Speed"] = df["Wind Speed"].round(
            0).astype(int).astype(str) + " kph"
        units = {
            "Temperature": "°C",
            "Humidity": "%",
            "Wind Speed": "kph",
        }
        df = df.rename(columns=units)
        # Sort by Time column in descending order
        df = df.sort_values("Time", ascending=False)
        st.table(df.tail(10))

        total_entries = len(df)
        st.write(f"Total Entries: {total_entries}")

# Function to calculate statistics for mood insights
def calculate_mood_statistics():
    if os.path.isfile(csv_file):
        df = pd.read_csv(csv_file)
        total_entries = len(df)
        happy_count = len(df[df["Mood"] == "😄 Happy"])
        neutral_count = len(df[df["Mood"] == "😐 Neutral"])
        sad_count = len(df[df["Mood"] == "😔 Sad"])

        mood_counts = {
            "Happy": happy_count,
            "Neutral": neutral_count,
            "Sad": sad_count
        }

        # Display mood statistics as a bar chart
        mood_counts = pd.DataFrame({"Mood": mood_counts.keys(), "Count": mood_counts.values()})
        st.bar_chart(mood_counts, x='Mood', y='Count' )

# Function to perform Linear Discriminant Analysis on weather data
def perform_lda(weather_data, mood_labels):
    le = LabelEncoder()
    y = le.fit_transform(mood_labels)
    lda = LinearDiscriminantAnalysis()
    lda.fit(weather_data, y)
    return lda

# Function to map mood labels to numerical values
def map_mood_labels(labels):
    encoder = LabelEncoder()
    encoded_labels = encoder.fit_transform(labels)
    return encoded_labels

# Function to calculate plane coefficients based on LDA
def calculate_plane_coefficients(lda):
    normal_vector = lda.coef_[0]
    d = lda.intercept_[0]
    return normal_vector, d

# Function to display the mood insights
def display_mood_insights():
    st.header("Mood Insights")
    calculate_mood_statistics()

    # Fetch weather data and mood labels
    if os.path.isfile(csv_file):
        df = pd.read_csv(csv_file)
        weather_data = df[["Temperature", "Humidity", "Wind Speed"]]
        mood_labels = df["Mood"]

        # Perform LDA on weather data
        lda = perform_lda(weather_data, mood_labels)

        # Get the significance of weather factors
        factors = weather_data.columns
        significance = np.abs(lda.coef_[0])
        sorted_indices = np.argsort(significance)[::-1]  # Sort in descending order

        # Display the most significant weather factors
        st.subheader("Most Significant Weather Factors on Mood:")
        for i in sorted_indices:
            factor = factors[i]
            factor_significance = significance[i]
            st.write(f"{factor}: {factor_significance:.2f}")

        # Visualize the significance as a bar chart
        significance_data = pd.DataFrame(
            {"Factor": factors[sorted_indices], "Significance": significance[sorted_indices]})
        st.bar_chart(significance_data, x="Factor", y="Significance")

        # Map mood labels to numerical values
        encoded_labels = map_mood_labels(mood_labels)

        # Calculate plane coefficients
        plane_normal, plane_d = calculate_plane_coefficients(lda)
        st.subheader("Your data all in one.")
        
        # Create a 3D scatter plot with hyperplane visualization
        fig = go.Figure(data=[
            go.Scatter3d(
                x=weather_data["Temperature"],
                y=weather_data["Humidity"],
                z=weather_data["Wind Speed"],
                mode="markers",
                marker=dict(
                    size=5,
                    color=encoded_labels,
                    colorscale="Viridis",
                    opacity=0.8
                ),
                name="Weather Data",
                text=mood_labels,
                hovertemplate="%{text}"
            ),
            go.Mesh3d(
                x=[-30, 40, 40, -30],
                y=[20, 20, 100, 100],
                z=[(-plane_normal[0]*(-30) - plane_normal[1]*20 - plane_d) / plane_normal[2],
                (-plane_normal[0]*40 - plane_normal[1]*20 - plane_d) / plane_normal[2],
                (-plane_normal[0]*40 - plane_normal[1]*100 - plane_d) / plane_normal[2],
                (-plane_normal[0]*(-30) - plane_normal[1]*100 - plane_d) / plane_normal[2]],
                i=[0, 1, 2, 0],
                j=[1, 2, 3, 1],
                k=[3, 0, 1, 3],
                opacity=0.3,
                color="rgba(255, 0, 0, 0.3)",
                name="Dividing Hyperplane"
            )
        ])

        fig.update_layout(
            scene=dict(
                xaxis_title="Temperature",
                yaxis_title="Humidity",
                zaxis_title="Wind Speed"
            ),
            margin=dict(l=0, r=0, b=0, t=0)
        )

        st.plotly_chart(fig)

        # Create a 2D projection of data points on the hyperplane
        projected_data = lda.transform(weather_data)
        projection_fig = px.scatter(x=projected_data[:, 0], y=projected_data[:, 1], color=mood_labels)
        projection_fig.update_layout(title="2D Projection on Hyperplane")
        st.plotly_chart(projection_fig)

        # # Display the hyperplane equation
        # x_label = f"{plane_normal[0]:.2f}*Temperature + {plane_normal[1]:.2f}*Humidity + {plane_normal[2]:.2f}*Wind Speed"
        # y_label = f"{plane_d:.2f}"
        # st.subheader("Hyperplane Equation:")
        # st.write(f"x-axis: {x_label}")
        # st.write(f"y-axis: {y_label}")


        # Funny insights based on the weather factors
        # st.subheader("Funny Insights")
        if factors[sorted_indices[0]] == "Temperature":
            if significance[sorted_indices[0]] > 0.5:
                st.markdown(
                    "<h3 style='font-weight:bold;'>You are a hot and spicy person! 🔥🌶️</h3>", unsafe_allow_html=True)
            else:
                st.markdown(
                    "<h3 style='font-weight:bold;'>You are as cool as a cucumber! 🥒❄️</h3>", unsafe_allow_html=True)
        elif factors[sorted_indices[0]] == "Humidity":
            if significance[sorted_indices[0]] > 0.5:
                st.markdown(
                    "<h3 style='font-weight:bold;'>You are a humidifier! 💦😅</h3>", unsafe_allow_html=True)
            else:
                st.markdown(
                    "<h3 style='font-weight:bold;'>You are a desert dweller. 🏜️😎</h3>", unsafe_allow_html=True)
        elif factors[sorted_indices[0]] == "Wind Speed":
            if significance[sorted_indices[0]] > 0.5:
                st.markdown(
                    "<h3 style='font-weight:bold;'>You are a tornado of energy! 🌪️⚡</h3>", unsafe_allow_html=True)
            else:
                st.markdown(
                    "<h3 style='font-weight:bold;'>You are as calm as a gentle breeze! 🍃😌</h3>", unsafe_allow_html=True)

    else:
        st.write("No mood entries available.")


# Main function to run the app
def main():
    st.title("Weather Mood Tracker App")
    st.sidebar.title("Track Your Mood")
    mood_options = ["😄 Happy", "😐 Neutral", "😔 Sad"]
    mood = st.sidebar.selectbox("Select Your Mood", mood_options)

    previous_time = 0
    if st.sidebar.button("What's my weather-mood"):
        if check_delta_time(previous_time):
            previous_time = time.time()
            data = fetch_weather_data(default_city)
            temperature = data["current"]["temp_c"]
            condition = data["current"]["condition"]["text"]
            humidity = data["current"]["humidity"]
            wind_speed = data["current"]["wind_kph"]
            # display_current_weather(default_city)
            add_entry(
                mood,
                temperature,
                condition,
                humidity,
                wind_speed,
            )
        else:
            st.sidebar.error(
                "Please wait at least 1 second before making another entry."
            )

    if st.sidebar.button("Delete Last Entry"):
        delete_last_entry()

    display_previous_entries()
    display_mood_insights()

    with st.sidebar:
        st.title('Current Weather')
        data = fetch_weather_data()
        temperature = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        humidity = data["current"]["humidity"]
        wind_speed = data["current"]["wind_kph"]

        st.write(f"Temperature: {temperature}°C")
        st.write(f"Condition: {condition}")
        st.write(f"Humidity: {humidity}%")
        st.write(f"Wind Speed: {wind_speed} kph")

        st.write(f"City: {default_city}")


if __name__ == "__main__":
    main()
