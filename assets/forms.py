from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Asset, Category
import os

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
    # File size limits (in bytes)
    MAX_ASSET_SIZE = 100 * 1024 * 1024  # 100MB
    MAX_THUMBNAIL_SIZE = 5 * 1024 * 1024  # 5MB
    
    ALLOWED_ASSET_EXTENSIONS = [
        '.zip', '.rar', '.7z', '.blend', '.fbx', '.obj', 
        '.png', '.jpg', '.jpeg', '.wav', '.mp3', '.ogg',
        '.cs', '.js', '.py', '.txt', '.md'
    ]
    
    ALLOWED_IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif', '.webp']
    
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
        self.fields['asset_file'].help_text = f"Upload your asset file (max {self.MAX_ASSET_SIZE // (1024*1024)}MB)"
        self.fields['thumbnail'].help_text = f"Upload a preview image (max {self.MAX_THUMBNAIL_SIZE // (1024*1024)}MB)"
    
    def clean_asset_file(self):
        file = self.cleaned_data.get('asset_file')
        if file:
            # Check file size
            if file.size > self.MAX_ASSET_SIZE:
                raise forms.ValidationError(f'Asset file too large. Maximum size is {self.MAX_ASSET_SIZE // (1024*1024)}MB.')
            
            # Check file extension
            file_extension = os.path.splitext(file.name)[1].lower()
            if file_extension not in self.ALLOWED_ASSET_EXTENSIONS:
                raise forms.ValidationError(f'Unsupported file type. Allowed types: {", ".join(self.ALLOWED_ASSET_EXTENSIONS)}')
        
        return file
    
    def clean_thumbnail(self):
        file = self.cleaned_data.get('thumbnail')
        if file:
            # Check file size
            if file.size > self.MAX_THUMBNAIL_SIZE:
                raise forms.ValidationError(f'Thumbnail too large. Maximum size is {self.MAX_THUMBNAIL_SIZE // (1024*1024)}MB.')
            
            # Check file extension
            file_extension = os.path.splitext(file.name)[1].lower()
            if file_extension not in self.ALLOWED_IMAGE_EXTENSIONS:
                raise forms.ValidationError(f'Unsupported image type. Allowed types: {", ".join(self.ALLOWED_IMAGE_EXTENSIONS)}')
        
        return file

