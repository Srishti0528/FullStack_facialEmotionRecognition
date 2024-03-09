import streamlit as st
import subprocess
import os
import time

st.title("Facial Emotion Recognition System")

process = None

if st.button("Start Facial Emotion Recognition"):
    process = subprocess.Popen(["python", "C:\\Users\\HP\\PycharmProjects\\frontend_facialEmotionRecognition\\testing.py"], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)

    st.write("Starting the process...")
    st.write("Thank you for trying our system...")

if st.button("Stop Facial Emotion Recognition"):
    if process is not None:
        process.terminate()

        # Wait for a short while to allow the other script to finish saving the graph
        time.sleep(2)

        st.write("Stopping the process...")
        st.write("Thank you using our system. Hope to see you back again:)")
    else:
        st.write("The process is not running.")
        st.write("OOPs, Something fishy")