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

# Dependency to connect with mongo db
import pymongo
import re


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
        try : 

            decMessage = fernet.decrypt(request.POST.get('encMessage')).decode()

            if self.ValidateID(decMessage):
                success = "true"
                message = decMessage
            else:
                success = "false"
                message = "Invalid Email QR Code!"

            response = {
                'Message':message,
                'success':success,
                }
        except:
            response = {
                'Message':"Invalid QR Code!",
                'success':"false",
                }

        return JsonResponse(response)

    def gen_fernet_key(self, passcode:bytes) -> bytes:
        assert isinstance(passcode, bytes)
        hlib = hashlib.md5()
        hlib.update(passcode)
        return base64.urlsafe_b64encode(hlib.hexdigest().encode('latin-1'))

    def ValidateID(self, idno):
        idPattern = '[0-9]{2}[a-zA-Z]{2}[0-9]{3}'

        if re.match(idPattern,idno):
            return True
        else:
            return False


        


class UpdateAjaxCall(View):

    def post(self, request):
        message = "null"
        try:
            client = pymongo.MongoClient('mongodb+srv://dikwickley:dikwickley077@cluster0.lnifa3d.mongodb.net/?retryWrites=true&w=majority')
            db = client['test']

            college_id = request.POST.get('ID')

            query = {"collegeid": college_id, "active": True}
            newval = {"$set": {"active": False}}

            if db.passes.update_one(query, newval):
                messgae = "Go...."
                success = "true"
            else:
                messgae = "This QR Code is Already Used Once!"
                success = "false"
        except:
            message = "Please try again!"
            success = "false"
        
        response = {
                'Message':message,
                'success':success,
                }
        return JsonResponse(response)

