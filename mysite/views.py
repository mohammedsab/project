from weasyprint import HTML
from django.utils import timezone
from datetime import timedelta
from django_weasyprint import WeasyTemplateResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.template.loader import render_to_string
from django.conf import settings


from .models import Passenger, Company
from .forms import HomePageForm, CompanyForm, PassengerModelForm

# Create your views here.


def index(request, anytext='0-1088-eyJpdiI6ImY4YU9iYkloenpqNTlZcjJCRGEyVmc9PSIsInZhbHVlIjoiZE5aaFZVXC9NaUxPS0dUcHJJUWVrWTI3aXllbUQwemUzRVc0UjZWbEtaY1djbmlHdU9ia0lSQmRVb0lCK1g1N2NnTzZiaU11dWlXWWFTajIySmRDNnFDUTZvUmlnM2NxU3p2dGpFT2NzRlJoUXo1dDFyWFwvcjltN1Rtek5DQ1hTMzBlQXpZNDZLaTYrS1FzNUsyNTNSdm1xUWFNb2ZwaTJHVmNLSVVTYk5ITHIyK1A4ZjkxTG41SnYrQmE5T2RaMFwvOGdGZXZLaVREemVPTW9ZUFlxQTN1NDRyXC9lMHJ5MlZLV3hheXJmM3FzVkpaWTFLXC9zZVwvcVNxSEppek9NelFVa1dnM21zNU9tcXBZWGJRUnNLdHB2NldmdlFQRElRbDZcL3VZNlwvbUNsN1pSb1dPd1A3cGpaVVFMbFdGS1dRNCtEWWZGeHlsT09aK1wvQ2FSeFpvMEJBRm5FTGl1c2ZGVkkweUZHRzhtK01mdWtcL0g5emVadVB5bHBIam9hSFV2T2doMDlCRXQweldJT2RRQXJrVTR0bDlrakZBb2VGUXo5WlFWVlJHZWVBVUxnYjNaRGtUTDI0MjNMWjVPOXl1cWVXN0NUMk9lQjMrVVNJZnhTVTlnXC8wVUlwUDFHZEFKMmdSeUxVTGlhZlBTQnlFaDhXZ0N3dzhBRzlOb05rZ3ZsQnE3S2hqYWJVQWlDdGN2eFFrZlwvXC93dnhqeGVadm5FRTl0bG1wRnBFSHlicmtDb0YrZHoxS01ZRU5wdlVyd3pnRk1PaEdRWU1BZk9HQ1NUOHIrSEhIXC8ySTVIWHhCc3FTUDJodGNsSkJmZElQNFdkY2VwY3dOQVZaVTdBRDNjQnpKVzhDWHV4QldcL05tUGo1ckdTYlh6ZXJzRUpTUVpkamVkMXFQSjd4dmJlNTdTN1k9IiwibWFjIjoiYjE1ZjJkM2I5YmI3Nzk1NjMzMDhiMTZkYmRiMDY0NDYzN2QyYzk3ODU2YzBjMDlmMjYyZWM5Njg4ZmJhYmVlMiJ9'):
    if request.method == 'POST':
        form = HomePageForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['search']
            passenger = Passenger.objects.filter(Q(national_id__icontains=query) | Q(
                passport_number__icontains=query) | Q(visa_number__icontains=query)).first()
            if passenger:
                return redirect('mysite:passenger_details', national_id=passenger.national_id)
            else:
                messages.error(request, 'لم يتم العثور علي بيانات')
                # form.add_error('search', 'passenger not found')
            # passengerDetails(pk=passenger.id)
                return render(request, 'mysite/index.html', {'form': form, 'section': 'index', })
    else:
        form = HomePageForm()
    return render(request, 'mysite/index.html', {'form': form, 'section': 'index'})


def passengerDetails(request, national_id):
    passenger = get_object_or_404(Passenger, national_id=national_id)
    one_week_from_now = passenger.created + timedelta(days=6)
    is_within_7_days = True
    now = timezone.now()
    delta = now - passenger.created
    if delta <= timedelta(days=7):
        is_within_7_days = False
    return render(request, 'mysite/passenger_details.html',
                  {'passenger': passenger, 'is_within_7_days': is_within_7_days, 'one_week_from_now': one_week_from_now})


def createPassenger(request):
    if request.method == 'POST':
        form = PassengerModelForm(request.POST)
        if not form.is_valid():
            return render(request, 'mysite/create_new_passenger.html', {'form': form, 'section': 'new_passenger'})

        else:
            form.save()
            return redirect('mysite:index')

    else:
        form = PassengerModelForm()
        return render(request, 'mysite/create_new_passenger.html', {'form': form, 'section': 'new_passenger'})


def passengerList(request):
    passengers = Passenger.objects.filter(deleted = False)
    if request.method == 'GET':
        search = request.GET.get('search')
        if search:
            passengers = passengers.filter(Q(national_id__icontains=search) |
                                           Q(passport_number__icontains=search) |
                                           Q(visa_number__icontains=search))
    return render(request, 'mysite/passenger_list.html', {'passengers': passengers, 'section': 'passenger_list'})


def passengerEdit(request, national_id):
    passenger = get_object_or_404(Passenger, national_id=national_id)
    if request.method == 'POST':
        form = PassengerModelForm(request.POST, instance=passenger)
        if form.is_valid():
            form.save()
            return redirect('mysite:index')
    else:
        form = PassengerModelForm(instance=passenger)
    return render(request, 'mysite/create_new_passenger.html', {'form': form, 'passenger': passenger, 'section': 'new_passenger'})


def passengerDelete(request, national_id):
    passenger = get_object_or_404(Passenger, national_id=national_id)
    if request.method == 'POST':
        passenger.deleted = True
        passenger.save()
        return redirect('mysite:passengerList')


def companyList(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()

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


def displayPDF(request, national_id):
    # Get some data from your Django application
    passenger = Passenger.objects.get(national_id=national_id)
    company_number = passenger.company.number

    data = {'passenger': passenger, 'company_number': company_number}
    # Render the HTML template using the data
    return render(request, 'mysite/pdf/pdf.html', data)
