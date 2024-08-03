import streamlit as st
import cv2
import numpy as np
from keras.models import load_model
import matplotlib.pyplot as plt
import io
import sqlite3

# Load the machine learning model
model = load_model('model_file3.h5')
faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

labels_dict = {0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Neutral', 5: 'Sad', 6: 'Surprise'}

# Initialize emotion counts
emotion_counts = {emotion: 0 for emotion in labels_dict.values()}

# Initialize connection to the database
conn = sqlite3.connect('userdata.db', check_same_thread=False)
c = conn.cursor()

# Create the table if it doesn't already exist
c.execute('''
    CREATE TABLE IF NOT EXISTS userdata
    (name TEXT, age INTEGER, gender TEXT, graphfile BLOB)
''')


# Define a function to capture and analyze the facial expressions
def analyze_face():
    video = cv2.VideoCapture(0)

    while True:
        ret, frame = video.read()
        if not ret:
            st.error("Failed to capture video.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)

        for x, y, w, h in faces:
            sub_face_img = gray[y:y + h, x:x + w]
            resized = cv2.resize(sub_face_img, (48, 48))
            normalize = resized / 255.0
            reshaped = np.reshape(normalize, (1, 48, 48, 1))
            result = model.predict(reshaped)
            label = np.argmax(result, axis=1)[0]

            # Update the count of the predicted emotion
            emotion_counts[labels_dict[label]] += 1

            # Display the resulting frame
            st.image(frame, channels="BGR")

    # When everything is done, release the capture
    video.release()
    cv2.destroyAllWindows()


# Define the app logic
def main():
    st.title("Facial Emotion Recognition")

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=100)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])

        if st.button("Login/Register"):
            # Check if the user exists in the database
            c.execute("SELECT * FROM userdata WHERE name = ? AND age = ?", (name, age))
            data = c.fetchone()
            if data is None:
                # Register the user
                c.execute("INSERT INTO userdata (name, age, gender) VALUES (?, ?, ?)", (name, age, gender))
                conn.commit()

            st.session_state['logged_in'] = True
            st.session_state['user_name'] = name
            st.success(f"Welcome {name}! You are now logged in.")

    else:
        # User is logged in, display the main app interface
        st.write(f"Welcome, {st.session_state['user_name']}!")
        if st.button("Start Facial Emotion Recognition"):
            analyze_face()

        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.session_state['user_name'] = None
            st.caching.clear_cache()


# Run the main function
if __name__ == "__main__":
    main()