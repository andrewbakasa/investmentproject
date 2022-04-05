import re

from common.models import Document, User
from django import forms
# from django.contrib.auth import authenticate, password_validation
# from django.contrib.auth.forms import PasswordResetForm


class DocumentForm(forms.ModelForm):
    teams_queryset = []
    teams = forms.MultipleChoiceField(choices=teams_queryset)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get("instance", None)
        request_obj = kwargs.pop("request_obj", None)
        users = kwargs.pop("users", [])
        super(DocumentForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}

        self.fields["status"].choices = [
            (each[0], each[1]) for each in Document.DOCUMENT_STATUS_CHOICE
        ]
        self.fields["status"].required = False
        self.fields["title"].required = True
        if users:
            self.fields["shared_to"].queryset = users
        self.fields["shared_to"].required = False
       

    class Meta:
        model = Document
        fields = ["title", "document_file", "status", "shared_to"]

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if not self.instance.id:
            if Document.objects.filter(title=title).exists():
                raise forms.ValidationError("Document with this Title already exists")
                return title
        if Document.objects.filter(title=title).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Document with this Title already exists")
            return title
        return title

