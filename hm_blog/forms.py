from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django.contrib.auth import authenticate
from hm_blog.models import ShotDetails, Comment, ContactFormModel

from PIL import Image

# get custom user

User = get_user_model()


class MyUserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput,
                                help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(MyUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class MyUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=_("Password"),
                                         help_text=_(
                                             "Raw şifrələr bazada saxlanmır, onları heç cürə görmək mümkün deyil "
                                             "bu istifadəçinin şifrəsidir, lakin siz onu dəyişə bilərsiziniz "
                                             " <a href=\"../password/\">bu form</a>. vasitəsilə"))

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MyUserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        return self.initial["password"]


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class": "input used form-control input-lg",
            "placeholder": "Password",
        }
    ))
    confirm_password = forms.CharField(label="Confirm password", widget=forms.PasswordInput(
        attrs={
            "class": "input used form-control input-lg",
            "placeholder": "Confirm Password",
        }
    ))

    def clean_re_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Password not match!!!")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'confirm_password', 'profile_image']

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control input-lg',
                "placeholder": "First Name"
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control input-lg',
                "placeholder": "Last Name"
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control input-lg',
                "placeholder": "Username"
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control input-lg',
                "placeholder": "Email address"
            })
        }


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control"
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class": "form-control"
        }
    ))


class ShotDetailForm(forms.ModelForm):
    class Meta:
        model = ShotDetails
        fields = ['Title', 'Preview_image', 'Description', 'tags', 'location', 'lisence', 'aspect']

        widgets = {
            'Title': forms.TextInput(attrs={
                'class': "form-control input-lg",
                'type': 'text',
                'placeholder': 'Title'
            }),
            'Preview_image': forms.TextInput(attrs={
                'class': "dropify",
                'type': 'file',
            }),

            'Description': forms.Textarea(attrs={
                'class': "form-control",
                'id': "input-desc",
                'rows': 6
            }),
            'tags': forms.Textarea(attrs={
                'class': "form-control",
                'rows': "3",
                'placeholder': "Tags..."
            }),
            'location': forms.TextInput(attrs={
                'type': "text",
                'class': "form-control",
                'placeholder': "Location"
            }),
            'lisence': forms.Select(attrs={
                'class': 'form-control'
            }),
            'aspect': forms.TextInput(attrs={
                'type': "text",
                'class': "form-control",
                'placeholder': "Aspect ratio, i.e. 4:3"
            })
        }

        labels = {
            'Title': 'Title',
            'Preview_image': 'Preview_image',
            'Description': 'Description'
        }

        span = {
            'Preview_image': 'The best image size is 800x600 pixels',
            # 'Images': 'Upload several images to show as an image gallery, if you`d like'
        }


class SettingProfileForm(forms.ModelForm):
    full_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'input2',
        'type': 'text'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'headline', 'location', 'description']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'input2',
                'type': 'text'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'input3',
                'type': 'email'
            }),
            'headline': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'input4',
                'type': 'text'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'input5',
                'type': 'text'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'input6',
                'type': 'text'
            })
        }
        labels = {
            'username': 'Username',
            'email': 'Email',
            'headline': 'Headline',
            'location': 'Location',
            'description': 'Description'
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

        widgets = {
            'comment': forms.TextInput(attrs={
                # 'type': "text",
                'class': "form-control",
                'placeholder': "Leave a comment...",
                'id': "comment"
            })
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactFormModel
        fields = ['name', 'email', 'message']

        widgets = {
            'name': forms.TextInput(attrs={
                'type': "text",
                'class': "form-control input-lg",
                'placeholder': "Name"
            }),
            'email': forms.EmailInput(attrs={
                'type': "email",
                'class': "form-control input-lg",
                'placeholder': "Email"
            }),
            'message': forms.Textarea(attrs={
                'class': "form-control",
                'rows': "5",
                'placeholder': "Message"
            })
        }
