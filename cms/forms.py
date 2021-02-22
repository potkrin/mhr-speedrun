from django.forms import ModelForm
from cms.models import Quest, Record
from django import forms

class QuestForm(ModelForm):
    """クエストのフォーム"""
    class Meta:
        model = Quest
        fields = ('questname', 'rank', 'target',)

class RecordForm(ModelForm):
    """記録のフォーム"""
    class Meta:
        model = Record 
        fields = ('quest', 'runner', 'party', 'cleartime', 'link', 'weapon', 'rules', 'platform', 'problems',)
        widgets = {
            'cleartime': forms.TextInput(attrs={'placeholder': '12:07.00'}),
        }


