# it is working correctly
import streamlit as st
import subprocess
import os
import sqlite3
import time

st.title("Facial Emotion Recognition System")

# Setup SQLite database
conn = sqlite3.connect('userdata.db')
c = conn.cursor()

# Create table if not exists
c.execute('''
    CREATE TABLE IF NOT EXISTS userdata
    (name TEXT, age INTEGER, gender TEXT, graphfile BLOB)
''')

# Login form
st.subheader('Login')
name = st.text_input('Name')
age = st.number_input('Age', min_value=1, max_value=100)
gender = st.selectbox('Gender', options=['Male', 'Female', 'Other'])
if st.button('Submit'):
    # Insert user data into database
    c.execute('''
        INSERT INTO userdata (name, age, gender) VALUES (?, ?, ?)
    ''', (name, age, gender))
    conn.commit()
    st.success('Logged in')

process = None  # Initialize the process variable

if st.button("Start Facial Emotion Recognition"):
    if os.path.exists("stop_sentinel.txt"):
        os.remove("stop_sentinel.txt")  # Remove the sentinel file if it exists
    # Pass the username as a command-line argument
    process = subprocess.Popen(["python", "C:\\Users\\HP\\PycharmProjects\\frontend_facialEmotionRecognition\\tes_graph_login.py", name], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    st.write("Starting the process...")
    st.write("Thank you for trying our system...")

if st.button("Stop Facial Emotion Recognition"):
    with open("stop_sentinel.txt", "w") as file:
        pass  # Create a sentinel file
    st.write("Stopping the process...")