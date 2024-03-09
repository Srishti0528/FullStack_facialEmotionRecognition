# import streamlit as st
# import subprocess
#
# st.title("Facial Emotion Recognition System")
#
# process = None
#
# if st.button("Start Facial Emotion Recognition"):
#     process = subprocess.Popen(["python", "C:\\Users\\HP\\PycharmProjects\\frontend_facialEmotionRecognition\\test.py"])
#     st.write("Starting the process...")
#
# if st.button("Stop Facial Emotion Recognition"):
#     if process is not None:
#         process.kill()
#         st.write("Stopping the process...")
#     else:
#         st.write("The process is not running.")





# import streamlit as st
# import subprocess
# import os
# import signal
#
# st.title("Facial Emotion Recognition System")
#
# if st.button("Start Facial Emotion Recognition"):
#     process = subprocess.Popen(["python", "C:\\Users\\HP\\PycharmProjects\\frontend_facialEmotionRecognition\\test.py"])
#     with open("process_id.txt", "w") as file:
#         file.write(str(process.pid))
#     st.write("Starting the process...")
#
# if st.button("Stop Facial Emotion Recognition"):
#     if os.path.exists("process_id.txt"):
#         with open("process_id.txt", "r") as file:
#             process_id = int(file.read())
#         os.kill(process_id, signal.SIGTERM)
#         st.write("Stopping the process...")
#     else:
#         st.write("The process is not running.")



import streamlit as st
import subprocess
import os
import signal
import time

st.title("Facial Emotion Recognition System")

if st.button("Start Facial Emotion Recognition"):
    process = subprocess.Popen(["python", "C:\\Users\\HP\\PycharmProjects\\frontend_facialEmotionRecognition\\test_graph3.py"], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    with open("process_id.txt", "w") as file:
        file.write(str(process.pid))
    st.write("Starting the process...")
    st.write("Thank you for trying our system...")

if st.button("Stop Facial Emotion Recognition"):
    if os.path.exists("process_id.txt"):
        with open("process_id.txt", "r") as file:
            process_id = int(file.read())
        os.kill(process_id, signal.CTRL_BREAK_EVENT)
        st.write("Stopping the process...")
        st.write("Thank you using our system. Hope to see you back again:)")
    else:
        st.write("The process is not running.")
        st.write("OOPs, Something fishy")



# if st.button("Stop Facial Emotion Recognition"):
#     if os.path.exists("process_id.txt"):
#         with open("process_id.txt", "r") as file:
#             process_id = int(file.read())
#         os.kill(process_id, signal.CTRL_BREAK_EVENT)
#
#         # Wait for a short while to allow the other script to finish saving the graph
#         time.sleep(2)
#
#         # Display the graph if it exists
#         if os.path.exists("emotion_counts.png"):
#             st.image("emotion_counts.png")
#
#         st.write("Stopping the process...")
#         st.write("Thank you using our system. Hope to see you back again:)")
#     else:
#         st.write("The process is not running.")
