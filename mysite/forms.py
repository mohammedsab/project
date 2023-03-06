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
                  'passport_start', 'passport_end', 'visa_type', 'visa_number', 'visa_start', 'visa_end', 'company',)
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

    def clean_national_id(self):
        national_id = self.cleaned_data['national_id']
        if not national_id.isnumeric() or len(national_id) != 14:
            raise forms.ValidationError('يجب ان الرقم القومي 14 رقم صحيح')
        return national_id

    def clean_passport_number(self):
        passport_number = self.cleaned_data['passport_number']
        if not passport_number.isalnum() or len(passport_number) != 8:
            raise forms.ValidationError('يجب ان يكون رقم جواز السفر 8 فقط')
        return passport_number

    def clean_visa_number(self):
        visa_number = self.cleaned_data['visa_number']
        if not visa_number.isnumeric() or len(visa_number) != 10:
            raise forms.ValidationError('يجب ان يكون رقم فيزا السفر 10 فقط')
        return visa_number

    def clean_passport_start(self):
        passport_start = self.cleaned_data['passport_start']
        if passport_start and passport_start < self.instance.created.date():
            raise forms.ValidationError(
                'يجب ان يكون التاريخ قبل اليوم')
        return passport_start

    def clean_passport_end(self):
        passport_end = self.cleaned_data['passport_end']
        if passport_end and passport_end < self.cleaned_data.get('passport_start'):
            raise forms.ValidationError(
                'يجب ان يكون التاريخ بعد اصدار جواز السفر')
        return passport_end

    def clean_visa_start(self):
        visa_start = self.cleaned_data['visa_start']
        if visa_start and visa_start < self.cleaned_data.get('passport_start'):
            raise forms.ValidationError(
                'يجب ان يكون التاريخ بعد اصدار جواز السفر')
        return visa_start

    def clean_visa_end(self):
        visa_end = self.cleaned_data['visa_end']
        if visa_end and visa_end < self.cleaned_data.get('visa_start'):
            raise forms.ValidationError(
                'يجب ان يكون التاريخ بعد اصدار التأشيرة')
        return visa_end


class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ('name', 'number')
        widgets = {
            'number': forms.NumberInput(attrs={'type': 'number'})
        }
