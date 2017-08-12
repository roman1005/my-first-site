from .models import UserHomePage
from django.forms import ModelForm
from django.core.files.images import get_image_dimensions
from django import forms


class ProfileForm(ModelForm):
    class Meta:
        model = UserHomePage
        exclude=('user_id',)

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']
        try:
            w, h = get_image_dimensions(avatar)

            # validate dimensions
            max_width = max_height = 100
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is '
                    '%s x %s pixels or smaller.' % (max_width, max_height))
        except AttributeError:
                """
                Handles case when we are updating the user profile
                and do not supply a new avatar
                """
                pass
                return avatar






