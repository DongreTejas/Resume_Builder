from django.shortcuts import redirect, render
from django.http import HttpResponse, FileResponse
from django.template import loader
from django.template.loader import render_to_string
import pdfkit
import io
import os
from .forms import ContactForm
from .models import Profile
from resumebuilder import settings
# Create your views here.


def accept(request):
    print(request.method)
    if request.method == "POST":
        profile_data = request.POST.dict()
        name = profile_data.get("Firstname")
        lastname = profile_data.get("lastname")
        phone = profile_data.get("phone", "")
        email = profile_data.get("email", "")
        website = profile_data.get("website", "")
        country = profile_data.get("country", "")
        aboutyou = profile_data.get("aboutyou", "")
        linkedin = profile_data.get("linkedin", "")
        github = profile_data.get("github", "")
        company = profile_data.get("company", "")
        company_exp = profile_data.get("company_exp", "")
        experience_title = profile_data.get("experience_title", "")
        hobbies = profile_data.get("hobbies", "")
        htmlskill = profile_data.get("htmlskill","")
        cssskill = profile_data.get("cssskill","")
        pythonskill = profile_data.get("pythonskill","")
        javascriptskill = profile_data.get("javascriptskill","")
        csskill = profile_data.get("csskill","")
        dbmsskill = profile_data.get("dbmsskill","")
        codingskill = profile_data.get("codingskill","")
        profile = Profile(name=name, lastname=lastname,phone=phone, email=email,website=website,country=country,linkedin=linkedin,github=github,company=company,company_exp=company_exp,experience_title=experience_title,hobbies=hobbies,aboutyou=aboutyou,htmlskill=htmlskill,cssskill=cssskill,pythonskill=pythonskill,javascriptskill=javascriptskill,csskill=csskill,dbmsskill=dbmsskill,codingskill=codingskill)
        profile.save()
        print(profile.id)
        return redirect('resume/' + str(profile.id))
    return render(request, "form.html")


def resume(request, id):
    user_profile = Profile.objects.get(pk=id)
    template = loader.get_template("resume.html")
    html = template.render({'user_profile': user_profile})
    option = {
        'page-size': 'Letter',
        'encoding': 'UTF-8'
    }
    pdf = pdfkit.from_string(html, False, option)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment'
    return response
    # return render(request, "resume.html", {'user_profile': user_profile})


def login(request):
    return render(request, "login.html")


def test(request, id):
    mydata = Profile.objects.get(id=id)
    print(mydata.name)
    template = loader.get_template('try.html')
    # template = loader.get_template('try_css.css')
    context = {
        'data': mydata
    }
    # html=template.render({'data': mydata})
    # option = {
    #     # 'page-size': 'Letter',
    #     # 'encoding': 'UTF-8',
    #     'enable-local-file-access': ""
    # }
    # config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    # pdf = pdfkit.from_string(html, False, option,configuration=config)
    # response = HttpResponse(pdf, content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment'
    # return response

   
    return HttpResponse(template.render(context, request))

	# return render(request, "try.html")
def download(request, id):
    bar=50
    mydata = Profile.objects.get(pk=id)
    print(mydata)
    template = loader.get_template('try.html')
    context = {
        'data': mydata,
        'b':bar
    }
    _html = render_to_string('try.html', context)
     # remove header
    _html = _html[_html.find('<body>'):]  

    # create new header
    new_header = '''<!DOCTYPE html>
    <html lang="ja">
    <head>
    <meta charset="utf-8"/>
    </head>
    <style>
'''
    # add style from css file. please change to your css file path.
    css_path = os.path.join(settings.BASE_DIR, 'myapp', 'static', 'try_css.css')
    with open(css_path, 'r') as f:
        new_header += f.read()
    new_header += '\n</style>'
    print(new_header)

    # add head to html
    _html = new_header + _html[_html.find('<body>'):]
    with open('try.html', 'w') as f: f.write(_html)  # for debug

    # convert html to pdf
    file_name = 'invoice.pdf'
    pdf_path = os.path.join(settings.BASE_DIR, 'myapp','static', file_name)
    config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    
    pdfkit.from_string(_html, pdf_path, options={"enable-local-file-access": ""}, configuration=config)
    return FileResponse(open(pdf_path, 'rb'), filename=file_name, content_type='application/pdf')

   
