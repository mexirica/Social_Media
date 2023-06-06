from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from allauth.account.forms import SignupForm
import logging
from .models import Photo


logger = logging.getLogger(__name__)
User = get_user_model()


from stdimage import StdImageField

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='Nome')
    last_name = forms.CharField(max_length=30, label='Sobrenome')
    profile_picture = forms.ImageField(label='Foto de perfil', required=False)
    username = forms.CharField(max_length=50, label="Nome de usuário", initial="user", required=False)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['username']
        if self.cleaned_data.get('profile_picture'):
            user.profile_picture.save(
                self.cleaned_data['profile_picture'].name,
                self.cleaned_data['profile_picture']
            )
        user.save()
        logger.info('Saved user %s', user.username)
        return user



    def clean(self):
        cleaned_data = super(CustomSignupForm, self).clean()
        email = cleaned_data.get('email')
        if email:
            try:
                self.validate_unique_email(email)
            except forms.ValidationError:
                self.add_error('email', "O email já está sendo utilizado. Por favor, tente outro email ou faça login com a sua conta existente.")
                self.account_already_exists = True
        return cleaned_data
    

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'subtitle', 'photo']

class PhotoEditForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'subtitle']