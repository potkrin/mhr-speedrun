from django.forms import ModelForm
from cms.models import Quest, Record, Issue
from django import forms
from django.core.validators import RegexValidator

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


class IssueForm(ModelForm):
    """記録のフォーム"""

    class Meta:
        model = Issue 
        fields = ('request', 'reason', 'detail',)
        widgets = {
            #'detail': forms.TextInput(attrs={'placeholder': 'Please input the issue detail.', 'rows':4, 'cols':15}),
            #'detail': forms.TextInput(attrs={'rows':4, 'cols':15}),
            'detail': forms.Textarea(attrs={'rows':4, 'cols':15, 'placeholder': 'Please input the issue detail here.'}),

        }



