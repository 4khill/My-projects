import cv2 
import numpy as np
import mtcnn
from .architecture import *
from .train_v2 import normalize,l2_normalizer
from scipy.spatial.distance import cosine
from tensorflow.keras.models import load_model
import pickle
import time
from collections import Counter
import os

class FaceDetector:
    def __init__(self, confidence_t=0.99, recognition_t=0.5, required_size=(160,160)):
        self.confidence_t = confidence_t
        self.recognition_t = recognition_t
        self.required_size = required_size
        self.face_encoder = InceptionResNetV2()
        path_m=os.path.abspath(__file__)
        path_m=os.path.dirname(path_m)
        path_m=os.path.join(path_m,"facenet_keras_weights.h5").replace("\\","/")
        #path_m = "C:/leo/Encryption Using Face/Face_detect/facenet_keras_weights.h5"
        self.face_encoder.load_weights(path_m)
        encodings_path=os.path.abspath(__file__)
        encodings_path=os.path.dirname(encodings_path).replace("\\","/")
        encodings_path=os.path.join(encodings_path,"encodings/encodings.pkl").replace("\\","/")
        #encodings_path = 'C:/leo/Encryption Using Face/Face_detect/encodings/encodings.pkl'
        self.face_detector = mtcnn.MTCNN()
        self.encoding_dict = self.load_pickle(encodings_path)

    @staticmethod
    def get_face(img, box):
        x1, y1, width, height = box
        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + width, y1 + height
        face = img[y1:y2, x1:x2]
        return face, (x1, y1), (x2, y2)

    def get_encode(self, face):
        face = normalize(face)
        face = cv2.resize(face, self.required_size)
        encode = self.face_encoder.predict(np.expand_dims(face, axis=0))[0]
        return encode

    @staticmethod
    def load_pickle(path):
        with open(path, 'rb') as f:
            encoding_dict = pickle.load(f)
        return encoding_dict

    def detect(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.face_detector.detect_faces(img_rgb)
        names = []
        for res in results:
            if res['confidence'] < self.confidence_t:
                continue
            face, pt_1, pt_2 = self.get_face(img_rgb, res['box'])
            encode = self.get_encode(face)
            encode = l2_normalizer.transform(encode.reshape(1, -1))[0]
            name = 'unknown'

            distance = float("inf")
            for db_name, db_encode in self.encoding_dict.items():
                dist = cosine(db_encode, encode)
                if dist < self.recognition_t and dist < distance:
                    name = db_name
                    distance = dist

            names.append(name)

            if name == 'unknown':
                cv2.rectangle(img, pt_1, pt_2, (0, 0, 255), 2)
                cv2.putText(img, name, pt_1, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
            else:
                cv2.rectangle(img, pt_1, pt_2, (0, 255, 0), 2)
                cv2.putText(img, name + f'__{distance:.2f}', (pt_1[0], pt_1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 200, 200), 2)
        return img, names

    def face_detect(self):
        cap = cv2.VideoCapture(0)
        start_time = time.time()
        all_names = []

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                print("CAM NOT OPEND") 
                break
            
            frame, names = self.detect(frame)
            all_names.extend(names)

            cv2.imshow('camera', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if time.time() - start_time > 10:
                break

        cap.release()
        cv2.destroyAllWindows()

        counter = Counter(all_names)
        most_common_name = counter.most_common(1)[0][0]
        return most_common_name