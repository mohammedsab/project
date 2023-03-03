from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q


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


# def compnayCreate(request):
#     if request.method == 'POST':
#         form = CompanyForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('mysite:company_list')
#     else:
#         form = CompanyForm
#     return render(request, 'mysite/company/create_company.html', {'form': form, 'section': 'company'})


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
        return redirect('company_list')
    return render(request, 'company_confirm_delete.html', {'company': company, 'section': 'company'})


