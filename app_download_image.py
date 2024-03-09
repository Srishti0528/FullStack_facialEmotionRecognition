# isko use kiya tha for getting downloadable link but it is not working properly.
import streamlit as st
import subprocess
import os
import sqlite3
import time
import base64
from PIL import Image
import io

st.title("Facial Emotion Recognition System")

# Function to create a download link for the image
def get_image_download_link(img, filename):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:image/png;base64,{img_str}" download="{filename}">Download image</a>'
    return href

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

# if st.button("Stop Facial Emotion Recognition"):
#     with open("stop_sentinel.txt", "w") as file:
#         pass  # Create a sentinel file
#     st.write("Stopping the process...")
#
#     # Retrieve the graph BLOB from the database
#     c.execute('SELECT graphfile FROM userdata WHERE name = ?', (name,))
#     graph_blob = c.fetchone()[0]
#
#     # Convert the BLOB back into an image
#     graph_image = Image.open(io.BytesIO(graph_blob))
#
#     # Display the image download link
#     st.markdown(get_image_download_link(graph_image, 'graph.png'), unsafe_allow_html=True)
if st.button("Stop Facial Emotion Recognition"):
    with open("stop_sentinel.txt", "w") as file:
        pass  # Create a sentinel file
    st.write("Stopping the process...")

    # Retrieve the graph BLOB from the database
    c.execute('SELECT graphfile FROM userdata WHERE name = ?', (name,))
    graph_blob = c.fetchone()[0]

    # Check if the graph_blob is not None
    if graph_blob is not None:
        try:
            # Convert the BLOB back into an image
            graph_image = Image.open(io.BytesIO(graph_blob))

            # Display the image download link
            st.markdown(get_image_download_link(graph_image, 'graph.png'), unsafe_allow_html=True)
        except Exception as e:
            st.write("Could not decode the image. Error:", str(e))
    else:
        st.write("No image found for this user.")