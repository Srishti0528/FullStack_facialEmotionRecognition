# import cv2
# import numpy as np
# from keras.models import load_model
# import matplotlib.pyplot as plt
# import streamlit as st
# import multiprocessing
# import os
# import signal
#
# # Global variable to store the process ID of the facial emotion recognition process
# # pid = None
# from streamlit.hashing import _CodeHasher
# from streamlit.report_thread import get_report_ctx
# from streamlit.server.server import Server
from streamlit.report_thread import get_report_ctx
from streamlit.server.server import Server


class SessionState(object):
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)


def get_session_state(**new_state):
    ctx = get_report_ctx()
    session_id = ctx.session_id
    session_info = Server.get_current()._get_session_info(session_id)

    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")

    if not hasattr(session_info, "session_state"):
        session_info.session_state = SessionState(**new_state)

    return session_info.session_state


def emotion_recognition():
    model = load_model('model_file3.h5')

    video = cv2.VideoCapture(0)

    face_detect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    labels_dict = {0:'Angry', 1:'Disgust', 2:'Fear', 3:'Happy', 4:'Neutral', 5:'Sad', 6:'Surprise'}

    emotion_counts = {emotion: 0 for emotion in labels_dict.values()}

    try:
        while True:
            ret, frame = video.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_detect.detectMultiScale(gray, 1.3, 5)
            for x, y, w, h in faces:
                sub_face_img = gray[y:y+h, x:x+w]
                resized = cv2.resize(sub_face_img,(48,48))
                normalize = resized/255.0
                reshaped = np.reshape(normalize, (1, 48, 48, 1))
                result = model.predict(reshaped)
                label = np.argmax(result, axis=1)[0]

                emotion_counts[labels_dict[label]] += 1

                emotion_probability = np.max(result)
                emotion_percentage = round(emotion_probability * 100, 2)

                cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 1)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(50,50,255),2)
                cv2.rectangle(frame,(x,y-40),(x+w,y),(50,50,255),-1)
                cv2.putText(frame, "{}: {}%".format(labels_dict[label], emotion_percentage), (x, y-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)

            cv2.imshow("Frame",frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Interrupted")

    finally:
        video.release()
        cv2.destroyAllWindows()

        plt.figure(figsize=(10, 5))

        colors = ['red', 'gray', 'lightblue', 'green', 'yellow', 'palegoldenrod', 'black']

        bars = plt.barh(list(emotion_counts.keys()), list(emotion_counts.values()), color=colors)

        plt.title('Emotion Counts')
        plt.xlabel('Count')
        plt.ylabel('Emotion')
        plt.grid(True)

        for bar in bars:
            plt.text(bar.get_width(), bar.get_y() + bar.get_height()/2,
                     f' {bar.get_width()}',
                     va='center', ha='left')

        plt.savefig('emotion_counts.png')
        plt.show()


@st.cache_data(allow_output_mutation=True)
def get_pid_dict():
    return {}


def main():
    session_state = get_session_state(pid=None)

    st.title("Facial Emotion Recognition System")

    if st.button("Start Facial Emotion Recognition"):
        if session_state.pid is None:
            process = multiprocessing.Process(target=emotion_recognition)
            process.start()
            session_state.pid = process.pid
            st.write("Starting the process...")
        else:
            st.write("The process is already running.")

    if st.button("Stop Facial Emotion Recognition"):
        if session_state.pid is not None:
            os.kill(session_state.pid, signal.SIGTERM)
            session_state.pid = None
            st.write("Stopping the process...")
        else:
            st.write("The process is not running.")

if __name__ == "__main__":
    main()