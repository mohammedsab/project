from django.urls import path

from . import views

app_name = 'mysite'

urlpatterns = [
    path('', views.index, name='index'),
    path('passenger/<str:national_id>',
         views.passengerDetails, name='passenger_details'),
    path("pdf/<str:national_id>/",
         views.index, name="detail_pdf"),
    path('new_passenger/', views.createPassenger, name='new_passenger'),

    path('company/', views.companyList, name='company_list'),
#     path('company/create/', views.compnayCreate, name='company_create'),
    path('company/<int:company_number>/edit/',
         views.companyEdit, name='company_edit'),
    path('company/<int:company_number>/delete/',
         views.companyDelete, name='company_delete'),
]
