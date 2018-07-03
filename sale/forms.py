from django import forms
from django.db.models import Q

from sale.models import Transfer, Position, Commdity, Stock, TemplateCategory, Patch

class TransferForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TransferForm, self).__init__(*args, **kwargs)
        status = kwargs['initial'].get('transfer_status', None)
        self.fields['transfer_status'].widget.choices = TemplateCategory.objects.filter(parent__code=status).values_list('code', 'title')
        self.fields['transfer_patch'] = forms.ChoiceField(label='批号')
        if status == '1000':
            self.fields['transfer_off'] = forms.CharField(label='折扣', widget=forms.TextInput())
        if status == '0110':
            self.fields['transfer_position'] = forms.CharField(label='门店', widget=forms.TextInput())

    def clean_transfer_code(self):
        code = self.cleaned_data.get('transfer_code', None)
        if code:
            raise forms.ValidationError('参数错误!')
        return code

    def clean_transfer_status(self):
        data = self.cleaned_data.get('transfer_status', None)
        if data or data in ['100001', '000101', '011001', '011002']:
            return data
        raise forms.ValidationError('参数错误!')

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = Transfer
        fields = '__all__'
        exclude = 'transfer_position', 'transfer_off'
        widgets = {
            'transfer_code': forms.TextInput(attrs={'onchange': 'getCode(this)'}),
            'transfer_patch': forms.Select(),
            'transfer_product': forms.Select(),
            'transfer_validity': forms.Select()
        }
        
class PatchForm(forms.ModelForm):
    
    
    def clean_patch_commdity(self):
        data = self.cleaned_data.get('patch_commdity', None)
        if not data:
            raise forms.ValidationError('错误!')
        return data
    
    
    class Meta:
        model = Patch
        fields = '__all__'
        widgets = {
            'patch_commdity': forms.TextInput(attrs={'readonly':''}),
        }