# this is our final code.....
# one more thing we can add that is login and register. if the user is new then they need to register and if old then
# they have to login and if user is old then there file will also be added in that graph field.
# but this is enhancement part, and we will
import streamlit as st
import subprocess
import os
import sqlite3
import time
#
# st.title("Facial Emotion Recognition System")
#
# # Check if 'logged_in' key exists in the session state
# if 'logged_in' not in st.session_state:
#     st.session_state['logged_in'] = False  # Initialize logged_in as False
#
# # Setup SQLite database
# conn = sqlite3.connect('userdata.db')
# c = conn.cursor()
#
# # Create table if not exists
# c.execute('''
#     CREATE TABLE IF NOT EXISTS userdata
#     (name TEXT, age INTEGER, gender TEXT, graphfile BLOB)
# ''')
#
# if not st.session_state['logged_in']:
#     # Login form
#     st.subheader('Login')
#     name = st.text_input('Name')
#     age = st.number_input('Age', min_value=1, max_value=100)
#     gender = st.selectbox('Gender', options=['Male', 'Female', 'Other'])
#     if st.button('Submit'):
#         # Insert user data into database
#         c.execute('''
#             INSERT INTO userdata (name, age, gender) VALUES (?, ?, ?)
#         ''', (name, age, gender))
#         conn.commit()
#         st.success('Logged in')
#         st.session_state['logged_in'] = True  # Update logged_in status
#         st.session_state['user_name'] = name  # Save user name in the session state
#
# else:
#     process = None  # Initialize the process variable
#
#     if st.button("Start Facial Emotion Recognition"):
#         if os.path.exists("stop_sentinel.txt"):
#             os.remove("stop_sentinel.txt")  # Remove the sentinel file if it exists
#         # Pass the username as a command-line argument
#         process = subprocess.Popen(["python", "C:\\Users\\HP\\PycharmProjects\\frontend_facialEmotionRecognition\\tes_graph_login.py", st.session_state['user_name']], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
#         st.write("Starting the process...")
#         st.write("Thank you for trying our system...")
#
#     if st.button("Stop Facial Emotion Recognition"):
#         with open("stop_sentinel.txt", "w") as file:
#             pass  # Create a sentinel file
#         st.write("Stopping the process...")



# if not st.session_state['logged_in']:
#     # Login form
#     st.subheader('Login')
#     name = st.text_input('Name')
#     age = st.number_input('Age', min_value=1, max_value=100)
#     gender = st.selectbox('Gender', options=['Male', 'Female', 'Other'])
#
#     # Setup SQLite database
#     conn = sqlite3.connect('userdata.db')
#     c = conn.cursor()
#
#     # Create table if not exists
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS userdata
#         (name TEXT, age INTEGER, gender TEXT, graphfile BLOB)
#     ''')
#
#     if st.button('Submit'):
#         # Insert user data into database
#         c.execute('''
#             INSERT INTO userdata (name, age, gender) VALUES (?, ?, ?)
#         ''', (name, age, gender))
#         conn.commit()
#         st.success('Logged in')
#         st.session_state['logged_in'] = True  # Update logged_in status
#         st.session_state['user_name'] = name  # Save user name in the session state
#
#         # Clear the input fields
#         st.empty()

# Check if 'logged_in' key exists in the session state
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False  # Initialize it as False

if not st.session_state['logged_in']:
    # Login form
    st.subheader('Login')
    name = st.text_input('Name')
    age = st.number_input('Age', min_value=1, max_value=100)
    gender = st.selectbox('Gender', options=['Male', 'Female', 'Other'])

    # Setup SQLite database
    conn = sqlite3.connect('userdata.db')
    c = conn.cursor()

    # Create table if not exists
    c.execute('''
        CREATE TABLE IF NOT EXISTS userdata
        (name TEXT, age INTEGER, gender TEXT, graphfile BLOB)
    ''')

    if st.button('Submit'):
        # Insert user data into database
        c.execute('''
            INSERT INTO userdata (name, age, gender) VALUES (?, ?, ?)
        ''', (name, age, gender))
        conn.commit()
        st.success('Logged in')
        st.session_state['logged_in'] = True  # Update logged_in status
        st.session_state['user_name'] = name  # Save user name in the session state

        # Clear the input fields
        st.empty()
else:
    st.write(f"Welcome, {st.session_state['user_name']}, hope you are well!! You can start the detection process by clicking on the start button")
    process = None  # Initialize the process variable

    if st.button("Start Facial Emotion Recognition"):
        if os.path.exists("stop_sentinel.txt"):
            os.remove("stop_sentinel.txt")  # Remove the sentinel file if it exists
        # Pass the username as a command-line argument
        process = subprocess.Popen(["python", "C:\\Users\\HP\\PycharmProjects\\frontend_facialEmotionRecognition\\tes_graph_login.py", st.session_state['user_name']], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        st.write("Starting the process...")
        st.write("Thank you for trying our system...")

    if st.button("Stop Facial Emotion Recognition"):
        with open("stop_sentinel.txt", "w") as file:
            pass  # Create a sentinel file
        st.write("Stopping the process...")

    if st.button("Back"):
        # Logout the user
        st.session_state['logged_in'] = False
        st.write("Going back to login page")
        # Clear the page
        st.empty()
