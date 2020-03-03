from PIL import Image
from django import forms
from .models import Picture


class PictureForm(forms.ModelForm):

    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Picture
        fields = ('file', 'x', 'y', 'width', 'height', )

    def save(self, commit=False):
        picture = super(PictureForm, self).save(commit=False)

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(picture.file)
        cropped_image = image.crop((x, y, w+x, h+y))
        cropped_image.save(picture.file.path)

        return picture
