# Dependencies to rensder the page
from django.shortcuts import render, HttpResponse
from django.views import View
from django.http import JsonResponse, StreamingHttpResponse # To return the captured frame to the web
import base64
from numpy import asarray

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

# class torender the scanning page
class StartScanning(View):
    template_name = 'QRScane/scan.html'

    def get(self, request):
        return render(request, self.template_name)

# class to handel the ajax for decode the data
class AjaxCall(View):
    def post(self, request):
        im_b64 = request.POST.get('image_data_url').split(',')[1]
        im_bytes = base64.b64decode(im_b64)
        image = asarray(im_bytes)
        # im_arr is one-dim Numpy array
        im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
        image = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
        print('this is smit patel')

        decoded_text = "null"
        continue_call = 'true'

        for code in decode(image):
            print('in the loop')
            decoded_data = code.data.decode('utf-8')
            if decoded_data:
                decoded_text = decoded_data
                continue_call = 'false'

        print(decoded_text)

        response = {
            'decoded_text': decoded_text,
            'continue_call': continue_call
        }
        return JsonResponse(response)