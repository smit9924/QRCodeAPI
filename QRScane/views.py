# Dependencies to rensder the page
from django.shortcuts import render, HttpResponse
from django.views import View
from django.http import StreamingHttpResponse # To return the captured frame to the web

# Dependencies to scan and capture qr code
from dbr import *
import threading
import cv2
import numpy as np
from pyzbar.pyzbar import decode

# Class to render the index page of the app QRScane
class QRScaneIndex(View):
    template_name = 'QRScane/index.html'

    def get(self, request):
        return render(request, self.template_name)

# Class to start the scanning
class StartScanning(View):
    template_name = 'QRScane/index.html/'

    # @gzip.gzip_page
    def get(self, request):
        try:
            cam = VideoCamera()
            return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
        except:
            pass
        cam = VideoCamera()
        return render(request, self.template_name)

# Class to capture video class
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        for code in decode(image):
            decoded_data = code.data.decode('utf-8')
            rect_pts = code.rect

            if decoded_data:
                if decoded_data == "True":
                    color = (0, 255, 0)
                    print_text = "Allow To Enter."
                elif decoded_data == "False":
                    color = (0, 0, 255)
                    print_text = "Deny To Enter."
                else:
                    color = (255, 0, 0)
                    print_text = "Not Detect!"

                pts = np.array([code.polygon], np.int32)
                cv2.polylines(image, [pts], True, (0, 255, 0), 3)
                cv2.putText(image, str(print_text), (rect_pts[0], rect_pts[1]), cv2.FONT_HERSHEY_COMPLEX, 1, color, thickness=3)
        success, jpeg = cv2.imencode('.jpeg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')