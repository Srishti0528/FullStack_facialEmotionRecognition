import cv2
import numpy as np
from keras.models import load_model
import matplotlib.pyplot as plt
import os
import sqlite3
import io
import sys

model = load_model('model_file3.h5')

video = cv2.VideoCapture(0)  # Use -1 to automatically select the default camera

faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

labels_dict = {0:'Angry', 1:'Disgust', 2:'Fear', 3:'Happy', 4:'Neutral', 5:'Sad', 6:'Surprise'}

# Initialize emotion counts
emotion_counts = {emotion: 0 for emotion in labels_dict.values()}

# Get the name of the user
name = sys.argv[1]

try:
    while True:
        # Check if stop_sentinel.txt file exists
        if os.path.exists("stop_sentinel.txt"):
            print("Stop signal received.")
            os.remove("stop_sentinel.txt")  # Remove the sentinel file
            break

        ret, frame = video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
        for x, y, w, h in faces:
            sub_face_img = gray[y:y+h, x:x+w]
            resized = cv2.resize(sub_face_img,(48,48))
            normalize = resized/255.0
            reshaped = np.reshape(normalize, (1, 48, 48, 1))
            result = model.predict(reshaped)
            label = np.argmax(result, axis=1)[0]

            # Update the count of the predicted emotion
            emotion_counts[labels_dict[label]] += 1

            # Get the percentage of the predicted emotion
            emotion_probability = np.max(result)
            emotion_percentage = round(emotion_probability * 100, 2)

            print("Emotion: {}, Confidence: {}%".format(labels_dict[label], emotion_percentage))

            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 1)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(50,50,255),2)
            cv2.rectangle(frame,(x,y-40),(x+w,y),(50,50,255),-1)
            cv2.putText(frame, "{}: {}%".format(labels_dict[label], emotion_percentage), (x, y-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)

        cv2.imshow("Frame",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Use cv2.waitKey(1) for video feeds
            break

    # Plot the emotion counts
    # plt.figure(figsize=(10, 5))
    # colors = ['red', 'gray', 'lightblue', 'green', 'yellow', 'palegoldenrod', 'black']
    # bars = plt.barh(list(emotion_counts.keys()), list(emotion_counts.values()), color=colors)
    # plt.title('Emotion Counts')
    # plt.xlabel('Count')
    # plt.ylabel('Emotion')
    # plt.grid(True)
    #
    # for bar in bars:
    #     plt.text(bar.get_width(), bar.get_y() + bar.get_height()/2,
    #              f' {bar.get_width()}',
    #              va='center', ha='left')
    #
    # # Save the plot to a BytesIO object
    # buf = io.BytesIO()
    # plt.savefig(buf, format='png')
    # plt.show()

    # Plot the emotion counts
    plt.figure(figsize=(10, 5))
    colors = ['red', 'gray', 'lightblue', 'green', 'yellow', 'palegoldenrod', 'black']
    bars = plt.bar(list(emotion_counts.keys()), list(emotion_counts.values()), color=colors)
    plt.title('Emotion Counts')
    plt.ylabel('Count')  # Adjust the label
    plt.xlabel('Emotion')  # Adjust the label
    plt.grid(True)

    for bar in bars:
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                 f' {int(bar.get_height())}',
                 ha='center', va='bottom')  # Adjust the label

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.show()

    # Continue with the rest of your code...

    # Convert the BytesIO object to a byte array
    buf.seek(0)
    graph_blob = buf.read()

    # Open the SQLite database and insert the graph BLOB
    conn = sqlite3.connect('userdata.db')
    c = conn.cursor()
    # c.execute('''
    #     UPDATE userdata SET graphfile = ? WHERE name = ?
    # ''', (sqlite3.Binary(graph_blob), name))
    # conn.commit()

    # new code part added for testing.
    c.execute('''
        UPDATE userdata SET graphfile = ? WHERE name = ?
    ''', (sqlite3.Binary(graph_blob), name))
    conn.commit()

except KeyboardInterrupt:  # Handle Ctrl+C
    print("Interrupted")

finally:  # This code runs whether the program ends normally or due to an exception
    video.release()
    cv2.destroyAllWindows()