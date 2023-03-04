from django.utils import timezone
from datetime import timedelta
import qrcode
from django_weasyprint import WeasyTemplateResponse
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
    is_within_7_days = True
    now = timezone.now()
    
    delta = now - passenger.created
    print(f'{now}--------{delta}')
    if delta <= timedelta(days=7):
        is_within_7_days = False
    return render(request, 'mysite/passenger_details.html', {'passenger': passenger, 'is_within_7_days': is_within_7_days})


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
    print(national_id, '********************')
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
            return redirect('mysite:company_list')
    else:
        form = CompanyForm(instance=company)
    return render(request, 'mysite/company/company_list.html', {'form': form, 'section': 'company'})


def companyDelete(request, company_number):
    company = get_object_or_404(Company, number=company_number)
    if request.method == 'POST':
        company.delete()
        return redirect('mysite:company_list')
    # return render(request, 'company_confirm_delete.html', {'company': company, 'section': 'company'})


def generate_qrcode(request):
    # assuming product number is passed as a GET parameter
    passenger_url = request.GET.get('passenger_url')
    qr = qrcode.QRCode(version=15, box_size=3, border=2)
    qr.add_data(f'{passenger_url}')
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    # width, height = img.size
    # img = img.resize((width*4, height*4), resample=0)
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response


def getPassengerPDF(request, national_id):
    # Get some data from your Django application
    passenger = Passenger.objects.get(national_id=national_id)
    data = {}

    # Render the HTML template using the data
    html_string = render_to_string(
        'mysite/pdf/pdf2.html', {'passenger': passenger})

    # Generate a PDF response using WeasyPrint
    response = WeasyTemplateResponse(request=request,
                                     template='mysite/pdf/pdf2.html',
                                     context={'passenger': passenger})

    # Set the response headers
    response['Content-Disposition'] = f'attachment; filename="{passenger.arabic_name}.pdf"'
    response['Content-Type'] = 'application/pdf'

    # Return the response
    return response
