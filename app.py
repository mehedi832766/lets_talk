from flask import Flask, request, render_template, send_file, Response
from werkzeug.utils import secure_filename
import io
from ultralytics import YOLO
import numpy as np
from PIL import Image
import cv2
import os
from datetime import datetime

now = datetime.now()
current_time = now.strftime("%H:%M:%S")


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
bangla_alphabets = [
    'অ', 'আ', 'ই', 'উ', 'এ', 
    'ও',  'ক', 'খ', 'গ', 'ঘ', 'চ',
      
   'ছ', 'জ', 'ঝ', 
    'ট', 'ঠ', 'ড', 'ঢ',  
    'ত', 'থ', 'ন',  
    'প', 'ফ', 'ব', 'ভ', 'ম', 
    'য়',  'র', 'ল', 'স', 'হ', 'ড়', 
    'ং',  'ঃ','joint', 
    'space', 'stop', 'দ', 'ধ'
]

def wordGen(lis=[]):
    ref=[]
    f=[]
    c = 0
    for index in range(len(lis)): 
        
        print("index number is: ",index)
        if len(ref)>0:
            print("ref size: ",len(ref))
            if ref[len(ref)-1]!=lis[index]:
                f.append(c)
                c=0
                ref.append(lis[index])
                c+=1
            else:
                c+=1
                continue
        else:
            c=c+1
            print(f"adding {index}th element")
            ref.append(lis[index])

    ls1 = []
    print(len(ref))
    ln=len(ref)
    ls1.append(ref[0]) 
    for i in range(1,ln-1):
        if ref[i-1] == ref[i+1] and f[i]<2:
            continue
        else:
            ls1.append(ref[i])    
    ls1.append(ref[ln-1])
    word = ''.join(ls1)
    file_path = "wordgen.txt"
    with open(file_path, "w") as file:
        file.write(str(word) + "\n")
    return word


class Detection:
    def __init__(self):
        #download weights from here:https://github.com/ultralytics/ultralytics and change the path
        self.model = YOLO("best.pt")

    def predict(self, img, classes=[], conf=0.35):
        if classes:
            results = self.model.predict(img, classes=classes, conf=conf, half=True )
        else:
            results = self.model.predict(img, conf=conf, half=True)

        return results

    def predict_and_detect(self, img, classes=[], conf=0.5, rectangle_thickness=2, text_thickness=1):
        results = self.predict(img, classes, conf=conf)
        clnm=""
        for result in results:
            for box in result.boxes:
                cv2.rectangle(img, (int(box.xyxy[0][0]), int(box.xyxy[0][1])),
                              (int(box.xyxy[0][2]), int(box.xyxy[0][3])), (255, 0, 0), rectangle_thickness)
                cv2.putText(img, f"{result.names[int(box.cls[0])]}",
                            (int(box.xyxy[0][0]), int(box.xyxy[0][1]) - 10),
                            cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), text_thickness)
                clnm=bangla_alphabets[int(box.cls[0])]
        return img, clnm
    def detect_from_image(self, image):
        result_img, clnm = self.predict_and_detect(image, classes=[], conf=0.4)
        return result_img,clnm


detection = Detection()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/object-detection/', methods=['POST'])
def apply_detection():
    if 'image' not in request.files:
        return 'No file part'

    file = request.files['image']
    if file.filename == '':
        return 'No selected file'

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        img = Image.open(file_path).convert("RGB")
        img = np.array(img)
        img = cv2.resize(img, (512, 512))
        img = detection.detect_from_image(img)
        output = Image.fromarray(img)

        buf = io.BytesIO()
        output.save(buf, format="PNG")
        buf.seek(0)

        os.remove(file_path)
        return send_file(buf, mimetype='image/png')

  # Add this at the top of your file with other globals



@app.route('/video')
def index_video():
    return render_template('video.html')


def gen_frames():
    file_path = "my_list.txt"
    cap = cv2.VideoCapture(0)
    letters = []
    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.resize(frame, (512, 512))
        if frame is None:
            break
        frame,clnm = detection.detect_from_image(frame)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        if clnm!='' and clnm!='space':
            letters.append(clnm)
        if clnm=='stop':
            break
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    letters.pop(len(letters)-1)
    current_word = (wordGen(letters) )
    with open(file_path, "w") as file:
        for item in letters:
            file.write(str(item)+"\n")
            # file.write(str(item) + " "+ str(current_time)+"\n")
    letters.clear()


@app.route('/get_word')
def get_word():
    if os.path.exists("wordgen.txt"):
        with open('wordgen.txt', 'r') as file:
                first_word = file.readline().strip()
    # if os.path.exists("wordgen.txt"):
    #     os.remove("wordgen.txt")
            
    return {'word': first_word}

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
    #http://localhost:8000/video for video source
    #http://localhost:8000 for image source
