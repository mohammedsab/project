from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from django.template.loader import render_to_string
from django.conf import settings

import weasyprint


from .models import Passenger, Company
from .forms import HomePageForm, CompanyForm, PassengerModelForm

# Create your views here.


def index(request):
    if request.method == 'POST':
        form = HomePageForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['search']
            passenger = Passenger.objects.filter(Q(national_id__icontains=query) | Q(
                passport_number__icontains=query) | Q(visa_number__icontains=query)).first()
            if passenger:
                return redirect('mysite:passenger_details', national_id=passenger.national_id)
            else:
                # messages.error(request, 'لم يتم العثور علي بيانات')
                form.add_error('search', 'passenger not found')
            # passengerDetails(pk=passenger.id)
                # return render(request, 'mysite/passenger_details.html', {'passenger': passenger})
    else:
        form = HomePageForm()
    return render(request, 'mysite/index.html', {'form': form, 'section': 'index'})


def passengerDetails(request, national_id):
    passenger = get_object_or_404(Passenger, national_id=national_id)
    return render(request, 'mysite/passenger_details.html', {'passenger': passenger})


def createPassenger(request):
    if request.method == 'POST':
        form = PassengerModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mysite:index')

    else:
        form = PassengerModelForm()
        return render(request, 'mysite/create_new_passenger.html', {'form': form, 'section': 'new_passenger'})


def passengerEdit(request, national_id):
    print(national_id,'********************')
    passenger = get_object_or_404(Passenger, national_id=national_id)
    if request.method == 'POST':
        form = PassengerModelForm(request.POST, instance=passenger)
        if form.is_valid():
            form.save()
            return redirect('mysite:index')
    else:
        form = PassengerModelForm(instance=passenger)
        print(form)
    return render(request, 'mysite/create_new_passenger.html', {'form': form, 'passenger': passenger, 'section': 'new_passenger'})


def passengerDelete(request, national_id):
    passenger = get_object_or_404(Passenger, national_id=national_id)
    if request.method == 'POST':
        passenger.delete()
        return redirect('mysite:index')
    # return render(request, 'company_confirm_delete.html', {'company': company, 'section': 'company'})


def companyList(request):

    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            # return render(request, 'mysite/company/company_list.html', { 'companies': companies, 'section': 'company'})

            return redirect('mysite:company_list')

    companies = Company.objects.all()
    form = CompanyForm()
    return render(request, 'mysite/company/company_list.html', {'form': form, 'companies': companies, 'section': 'company'})


def companyEdit(request, company_number):
    company = get_object_or_404(Company, number=company_number)
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect('company_list')
    else:
        form = CompanyForm(instance=company)
    return render(request, 'mysite/company_edit.html', {'form': form, 'section': 'company'})


def companyDelete(request, company_number):
    company = get_object_or_404(Company, number=company_number)
    if request.method == 'POST':
        company.delete()
        return redirect('mysite:company_list')
    # return render(request, 'company_confirm_delete.html', {'company': company, 'section': 'company'})


# def getPassengerPDF(request, national_id):
#     passenger = get_object_or_404(Passenger, national_id=national_id)
#     html = render_to_string('mysite/pdf/pdf.html', {'passenger':passenger})

#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'filename={passenger.arabic_name}.pdf'

#     weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')])
#     return response


# from django.http import HttpResponse
# from django.template.loader import render_to_string
from django_weasyprint import WeasyTemplateResponse
import qrcode


def generate_qrcode(request):
    # assuming product number is passed as a GET parameter
    national_id = request.GET.get('national_id')
    qr = qrcode.QRCode(version=1, box_size=2, border=2)
    qr.add_data('mohammed saber awadmohammed saber awadmohammed saber awadmohammed saber awadmohammed saber awadmohammed saber awadmohammed saber awadmohammed saber awadmohammed saber awadmohammed saber awad')
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    # width, height = img.size
    # img = img.resize((width*4, height*4), resample=0)
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response

def getPassengerPDF(request, national_id):
    # Get some data from your Django application
    data = {}

    # Render the HTML template using the data
    html_string = render_to_string('mysite/pdf/pdf2.html', {'data': data})

    # Generate a PDF response using WeasyPrint
    response = WeasyTemplateResponse(request=request, 
                                     template='mysite/pdf/pdf2.html', 
                                     context={'data': data})

    # Set the response headers
    response['Content-Disposition'] = 'attachment; filename="my_document.pdf"'
    response['Content-Type'] = 'application/pdf'

    # Return the response
    return response
