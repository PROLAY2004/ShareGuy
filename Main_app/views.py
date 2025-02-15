from django.shortcuts import render,HttpResponse,redirect
import random
from datetime import timedelta
from django.utils.timezone import now
from django.http import FileResponse
from django.conf import settings
from django.core.files import File
from django.core.mail import EmailMessage,send_mail
from .models import data_records
import qrcode 
import os

# Create your views here.
def index(request):
    return redirect("Home")

def ucode():
    key = str(random.randint(100000,999999))
    if(data_records.objects.filter(code = key).exists()):
        return ucode()
    else:
        return key

def home(request):
    file = request.FILES.get("file")
    recive_code = request.POST.get("reciver_code")
    email = request.POST.get("email")
    file_id = request.POST.get("mail_code")

    if(email and file_id):
        data = data_records.objects.get(code = file_id)
        mail_file = data.file
        mail_obj = EmailMessage(
            subject="Email from ShareGuy",
            body="Here is your file which you have shared using ShareGuy. Thanks for using our service.",
            from_email="shareguy@shareguy.whf.bz",
            to=[email],
            )
        mail_obj.attach_file(mail_file.path)
        mail_obj.send(fail_silently=False)
        data.file.delete()
        data.qr.delete()
        data.delete()
        return redirect("Home")
    if(file):
        if(file.size>20*1024*1024):
            context ={
                "bool" : 0,
                "message" : "Max File Size 20MB"
            }
            return render(request,'home.html',context)
        else:
            unicode = ucode()
            full_url = request.build_absolute_uri()
            data = full_url.replace("Home","") + "Download/"+ unicode
            # data = "https://74fwdvvb-8000.inc1.devtunnels.ms/Download/"+ unicode
            qrc = qrcode.QRCode(
                version=1,  # Control the size of the QR code (1 is the smallest size)
                error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
                box_size=10,  # Size of each box in the QR code
                border=4,  # Thickness of the border
            ) 
            qrc.add_data(data)
            qrc.make(fit=True) # ---> This is optional

            img = qrc.make_image(fill='black', back_color='white')
            qr_name = unicode + ".png"

            if not os.path.exists(settings.MEDIA_ROOT):
                os.makedirs(settings.MEDIA_ROOT) 

            output = os.path.join(settings.MEDIA_ROOT,qr_name)
            img.save(output)

            with open(output, "rb") as f:
                data_records.objects.create(file = file, code = unicode, qr = File(f, name=qr_name), inserttime = now())

            os.remove(output)
            context ={
                "bool" : 1,
                "code" : unicode,
                "qr" : data_records.objects.get(code = unicode).qr,
            }
            return render(request,'home.html',context)
    elif(recive_code):
        if(data_records.objects.filter(code = recive_code).exists()):
            data = data_records.objects.get(code = recive_code)
            file_path = data.file.path
            return FileResponse(open(file_path,"rb"),filename=data.file.name,as_attachment=True)
        else:
            context ={
                "bool" : 0,
                "message" : "Invalid Code or Code Expired."
                }
            return render(request,'home.html',context)
        
    for i in data_records.objects.all():
        time_difference = now() - i.inserttime
        if(time_difference > timedelta(minutes=5)):
            i.file.delete()
            i.qr.delete()
            i.delete()
            
    context ={
        "bool" : 0
    }
    return render(request,'home.html',context)


def about(request):
    return render(request,'about.html')


def contact(request):
    name = request.POST.get("name")
    email = request.POST.get("email")
    message = request.POST.get("message")
    if(name and email and message):
        send_mail(
            "Contact US - ShareGuy",
            "From " + name + " ( " + email + " ) " + "; Message : " + message,
            'shareguy@shareguy.whf.bz',
            ['prolayhalder2004@gmail.com'],
            fail_silently= False,
        )
        context = {
            "message" : "Message Sent ! Thanks For Contacting."
        }
        return render(request,'contact.html',context)
    else:
        return render(request,'contact.html')


def qr_download(request,code):
    if(data_records.objects.filter(code = code).exists()):
        data = data_records.objects.get(code = code)
        file_path = data.file.path
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=data.file.name)
    else:
        return HttpResponse("Invalid QR data.")
    
