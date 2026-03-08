from django import forms

from wagtail.users.forms import UserEditForm, UserCreationForm

class CustomUserEditForm(UserEditForm):
    bio = forms.CharField(label="Biografía", widget=forms.Textarea)
    profile_picture = forms.ImageField(label="Foto de perfil", widget=forms.ImageField)

    class Meta:
        fields = UserEditForm.Meta.fields | {"bio", "profile_picture"}

class CustomUserCreationForm(UserCreationForm):
    bio = forms.CharField(label="Biografía", widget=forms.Textarea)
    profile_picture = forms.ImageField(label="Foto de perfil", widget=forms.ImageField)

    class Meta:
        fields = UserEditForm.Meta.fields | {"bio", "profile_picture"}