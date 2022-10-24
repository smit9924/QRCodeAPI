# Dependencies to render the page
from django.shortcuts import render, HttpResponse
from django.views import View
from django.template.loader import render_to_string
import json

# Dependency to generate the QR Code
import qrcode
from io import BytesIO

# Dependencies to send the Email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import smtplib
from QRCodeAPI import settings

# Dependency to math string wiht the regex
import re


# Class that render the index page of the app QRGenerate
class QRGenerateIndex(View):
    template_name = 'QRGenerate/index.html'

    def get(self, request):
        return render(request, self.template_name)

# Class to create QR Code and send the Email
class QRGenerator(View):
    template_name = 'QRGenerate/EmailTemplate.html'

    def get(self, request, email, aligibility):
        # calling the method to generate the QRCode
        img = self.QRCodeGenerate(aligibility)

        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.match(pattern,email):
            # Calling method to send the email
            if self.SendEmail(email, img) :
                EmailSent = True
                Error = None
        else :
            EmailSent = False
            Error = "Invalid email address."

        return HttpResponse(json.dumps({'EmailSent': EmailSent, 'Error': Error}),
                       content_type="application/json")
    
    # This method will generate the QR Code and return the PIL Image Object
    def QRCodeGenerate(self, data):
        # Making the QR Code Data
        QR_Data = data
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
        qr.add_data(QR_Data)
        qr.make(fit=True)
        img=qr.make_image(fill_color='black', back_color='white').convert('RGB')
        # img.save('static/QRCode.png')

        return img

    # This method will send the E-mail if the given mail address is pass the validation
    def SendEmail(self, email, img):
        # Create the root message and set the details
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = 'This is the E-mail from team Genesis'
        msgRoot['From'] = 'smitpatel2301322002@gmail.com'
        msgRoot['To'] = 'smit.dpatel9924@gmail.com'
        msgRoot.preamble = 'This is the multipart message in the form of MIME format'

        msgALternative = MIMEMultipart('alternative')
        msgRoot.attach(msgALternative)

        # Generating the HTML code
        msgText = MIMEText(render_to_string(self.template_name), 'html') # Alternatively we can write HTML content here instead of render_to_string function
        msgALternative.attach(msgText)
        
        # Reading the image file
        byte_buffer = BytesIO() # Set buffer to the Byte stream
        img.save( byte_buffer, 'PNG') # Convert PIL Image object into the Byte object
        msgImage = MIMEImage(byte_buffer.getvalue()) # Converting the QR Code into MIMEImage object without saving the image

        # Attach the image's content ID
        msgImage.add_header('Content-ID', '<image1>')
        msgRoot.attach(msgImage)

        # Generating SMTP server and sending the email
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.starttls()
        server.login(settings.EMAIL_HOST_USER,settings.EMAIL_HOST_PASSWORD)
        server.sendmail(settings.EMAIL_HOST_USER, email, msgRoot.as_string())
        server.quit()

        return True
