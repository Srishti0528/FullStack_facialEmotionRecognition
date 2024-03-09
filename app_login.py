# import streamlit as st
# import subprocess
# import os
# import sqlite3
# import signal
# import time
#
# st.title("Facial Emotion Recognition System")
#
# # Setup SQLite database
# conn = sqlite3.connect('userdata.db')
# c = conn.cursor()
#
# # Create table if not exists
# c.execute('''
#     CREATE TABLE IF NOT EXISTS userdata
#     (name TEXT, age INTEGER, gender TEXT, graphfile TEXT)
# ''')
#
# # Login form
# st.subheader('Login')
# name = st.text_input('Name')
# age = st.number_input('Age', min_value=1, max_value=100)
# gender = st.selectbox('Gender', options=['Male', 'Female', 'Other'])
# if st.button('Submit'):
#     # Insert user data into database
#     c.execute('''
#         INSERT INTO userdata (name, age, gender) VALUES (?, ?, ?)
#     ''', (name, age, gender))
#     conn.commit()
#     st.success('Logged in')
#
# if st.button("Start Facial Emotion Recognition"):
#     process = subprocess.Popen(["python", "C:\\Users\\HP\\PycharmProjects\\frontend_facialEmotionRecognition\\test_graph3.py"], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
#     with open("process_id.txt", "w") as file:
#         file.write(str(process.pid))
#     st.write("Starting the process...")
#     st.write("Thank you for trying our system...")
#
# if st.button("Stop Facial Emotion Recognition"):
#     if os.path.exists("process_id.txt"):
#         with open("process_id.txt", "r") as file:
#             process_id = int(file.read())
#         os.kill(process_id, signal.CTRL_BREAK_EVENT)
#
#         # Save path to graph in database
#         graphfile = 'emotion_counts.png'
#         c.execute('''
#             UPDATE userdata SET graphfile = ? WHERE name = ?
#         ''', (graphfile, name))
#         conn.commit()
#
#         st.write("Stopping the process...")
#         st.write("Thank you using our system. Hope to see you back again:)")
#     else:
#         st.write("The process is not running.")
#         st.write("OOPs, Something fishy")

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
    (name TEXT, age INTEGER, gender TEXT, graphfile TEXT)
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

# if st.button("Start Facial Emotion Recognition"):
#     process = subprocess.Popen(["python", "C:\\Users\\HP\\PycharmProjects\\frontend_facialEmotionRecognition\\test_graph3.py"], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
#     st.write("Starting the process...")
#     st.write("Thank you for trying our system...")
#
# if st.button("Stop Facial Emotion Recognition"):
#     if process is not None:
#         process.terminate()
#
#         # Save path to graph in database
#         graphfile = 'emotion_counts.png'
#         c.execute('''
#             UPDATE userdata SET graphfile = ? WHERE name = ?
#         ''', (graphfile, name))
#         conn.commit()
#
#         st.write("Stopping the process...")
#         st.write("Thank you using our system. Hope to see you back again:)")
#     else:
#         st.write("The process is not running.")
#         st.write("OOPs, Something fishy")

if st.button("Start Facial Emotion Recognition"):
    if os.path.exists("stop_sentinel.txt"):
        os.remove("stop_sentinel.txt")  # Remove the sentinel file if it exists
    process = subprocess.Popen(["python", "C:\\Users\\HP\\PycharmProjects\\frontend_facialEmotionRecognition\\test_graph33.py"], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    st.write("Starting the process...")
    st.write("Thank you for trying our system...")

if st.button("Stop Facial Emotion Recognition"):
    with open("stop_sentinel.txt", "w") as file:
        pass  # Create a sentinel file
    st.write("Stopping the process...")