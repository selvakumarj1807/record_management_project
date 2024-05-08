from django import forms  
from record_management_app.models import Record  
class RecordForm(forms.ModelForm):  
    class Meta:  
        model = Record  
        fields = ['company_name', 'company_code', 'email', 'strength', 'website'] 
        widgets = { 'company_name': forms.TextInput(attrs={ 'class': 'form-control' }), 
            'email': forms.EmailInput(attrs={ 'class': 'form-control' }),
            'company_code': forms.TextInput(attrs={ 'class': 'form-control' }),
            'website': forms.TextInput(attrs={ 'class': 'form-control' }),
            'strength': forms.TextInput(attrs={ 'class': 'form-control' }),
      }