from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Asset, Category

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes for styling
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class AssetUploadForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ('title', 'description', 'category', 'asset_file', 'thumbnail')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter asset title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your asset...',
                'rows': 4
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'asset_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.zip,.rar,.7z,.blend,.fbx,.obj,.png,.jpg,.wav,.mp3,.cs,.js,.py'
            }),
            'thumbnail': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].empty_label = "Select a category"
        
        # Add help text
        self.fields['asset_file'].help_text = "Upload your asset file (ZIP, RAR, 7Z, Blend, FBX, OBJ, images, audio, scripts)"
        self.fields['thumbnail'].help_text = "Upload a preview image for your asset"

