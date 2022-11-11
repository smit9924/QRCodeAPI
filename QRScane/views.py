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

# Dependency to decode the data
from cryptography.fernet import Fernet
import hashlib, base64

# Class to render the index page of the app QRScane
class QRScaneIndex(View):
    template_name = 'QRScane/index.html'
    
    def get(self, request):
        return render(request, self.template_name)

# class torender the scanning page
class StartScanning(View):
    # template_name = 'QRScane/scan.html'
    template_name = 'QRScane/scaneThanganat.html'

    def get(self, request):
        return render(request, self.template_name)

# class to handel the ajax for decode the data
class AjaxCall(View):

    def post(self, request):
        key = "smit"
        key = self.gen_fernet_key(key.encode('utf-8'))
        fernet = Fernet(key)
        decMessage = fernet.decrypt(request.POST.get('encMessage')).decode()

        response = {
            'Message':decMessage,
            'Success':'true/false',
            }
        return JsonResponse(response)

    def gen_fernet_key(self, passcode:bytes) -> bytes:
        assert isinstance(passcode, bytes)
        hlib = hashlib.md5()
        hlib.update(passcode)
        return base64.urlsafe_b64encode(hlib.hexdigest().encode('latin-1'))





















# class AjaxCall(View):

#     def post(self, request):
#         im_b64 = request.POST.get('image_data_url').split(',')[1]
#         im_bytes = base64.b64decode(im_b64)
#         image = asarray(im_bytes)
#         # im_arr is one-dim Numpy array
#         im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
#         image = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
#         print('this is smit patel')

#         decoded_text = "null"
#         continue_call = 'true'

#         for code in decode(image):
#             print('in the loop')
#             decoded_data = code.data.decode('utf-8')
#             if decoded_data:
#                 decoded_text = decoded_data
#                 continue_call = 'false'

#         print(decoded_text)

#         response = {
#             'decoded_text': decoded_text,
#             'continue_call': continue_call
#         }
#         return JsonResponse(response)



# from cryptography.fernet import Fernet

# # we will be encrypting the below string.
# message = "hello geeks"

# # generate a key for encryption and decryption
# # You can use fernet to generate
# # the key or use random key generator
# # here I'm using fernet to generate key

# key = Fernet.generate_key()

# # Instance the Fernet class with the key

# fernet = Fernet(key)

# # then use the Fernet class instance
# # to encrypt the string string must
# # be encoded to byte string before encryption
# encMessage = fernet.encrypt(message.encode())

# print("original string: ", message)
# print("encrypted string: ", encMessage)

# # decrypt the encrypted string with the
# # Fernet instance of the key,
# # that was used for encrypting the string
# # encoded byte string is returned by decrypt method,
# # so decode it to string with decode methods
# decMessage = fernet.decrypt(encMessage).decode()

# print("decrypted string: ", decMessage)
