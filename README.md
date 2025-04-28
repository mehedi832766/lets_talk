# 🤟 Lets Talk : Bangla Sign Language to Text Converter

A real-time web application built with Flask that translates **Bangla Sign Language (BSL)** into **Bangla words** using a custom-trained **YOLOv8 object detection model**. This project empowers communication accessibility for the hearing-impaired community through vision-based AI.

## 🧠 Project Description

- Developed a Flask-based web application that processes video streams in real-time to recognize Bangla Sign Language gestures.
- YOLOv8 model was trained on a self-collected dataset of **2000+ labeled images** representing Bangla alphabet signs.
- Recognized signs are translated into corresponding Bangla words and displayed instantly.

## ✨ Key Features

- 🔍 Real-time gesture recognition using a webcam feed  
- 🧠 YOLOv8 model for high-speed and accurate sign detection  
- 📝 Generates readable Bangla text from recognized gestures  
- 🌐 User-friendly web interface using HTML5 + JavaScript  
- 📦 Modular Flask backend with easy deployment  

## 🛠 Tech Stack

- **Frontend**: HTML, Tailwind, JavaScript (Webcam streaming)  
- **Backend**: Python, Flask  
- **Model**: YOLOv8 (Ultralytics)  
- **Training Data**: 2000+ custom labeled Bangla sign language gesture images  

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/bangla-sign-language-webapp.git
cd bangla-sign-language-webapp
```

### 2. Create & Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Download Trained YOLOv8 Model
Place your best.pt file (YOLOv8 trained weights) in the models/ directory.

### 5. Run the Application
```bash
python app.py
```
Navigate to http://127.0.0.1:5000 in your browser to use the app.

## 📸 Demo Video
https://github.com/user-attachments/assets/2a735480-bcc8-43e3-87a3-3a1a64bed5a2

## 🧠 Model Training Overview

- **Model**: YOLOv8 (from Ultralytics)  
- **Dataset**: 2000+ labeled images across multiple Bangla letters  
- **Tools**: Roboflow for annotation, Ultralytics for training  
- **Augmentation**: Rotation, Flip, Brightness  
- **Accuracy**: >95% mAP on validation set  

## 📌 Acknowledgements

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- [Flask](https://flask.palletsprojects.com/en/stable/)


