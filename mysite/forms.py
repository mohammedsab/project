from django import forms
from captcha.fields import ReCaptchaField


from .models import Passenger, Company


class HomePageForm(forms.Form):
    search = forms.CharField(
        label='رقم جواز السفر / الرقم القومى', widget=forms.TextInput(attrs={'placeholder': '********************'}))
    captcha = ReCaptchaField()


# ('arabic_name', 'english_name', 'national_id', 'data_of_birth', 'passport_number',
#  'passport_start', 'passport_end', 'visa_type', 'visa_number', 'visa_start', 'visa_end', )


class PassengerModelForm(forms.ModelForm):
    CHOICES = (
        ('option1', 'Option 1'),
        ('option2', 'Option 2'),
        ('option3', 'Option 3'),
    )
    # visa_type = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label='نوع الفيزا')

    class Meta:
        model = Passenger
        fields = ('arabic_name', 'english_name', 'national_id', 'data_of_birth', 'passport_number',
                    'passport_start', 'passport_end', 'visa_type', 'visa_number', 'visa_start', 'visa_end', 'company',  )
        labels = {
            'arabic_name': 'الاسم بالعربي',
            'english_name': 'الاسم الإنجليزية',
            'national_id': 'رقم القومي',
            'data_of_birth': 'تاريخ الميلاد',
            'passport_number': 'رقم الجواز',
            'passport_start': 'تاريخ الاصدار',
            'passport_end': 'تاريخ الانتهاء',
            'visa_type': 'نوع الفيزا',
            'visa_number': 'رقم الفيزا',
            'visa_start': 'تاريخ الاصدار',
            'visa_end': 'تاريخ الانتهاء',
            'company': 'الشركة',
        }
        widgets = {
            'national_id': forms.NumberInput(attrs={'type': 'number'}),
            'visa_number': forms.NumberInput(attrs={'type': 'number'}),
            'data_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'passport_start': forms.DateInput(attrs={'type': 'date'}),
            'passport_end': forms.DateInput(attrs={'type': 'date'}),
            'visa_start': forms.DateInput(attrs={'type': 'date'}),
            'visa_end': forms.DateInput(attrs={'type': 'date'}),
        }


class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ('name', 'number')
        widgets = {
            'number': forms.NumberInput(attrs={'type':'number'})
        }
