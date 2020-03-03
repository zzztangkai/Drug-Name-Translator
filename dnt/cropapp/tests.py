from io import StringIO, BytesIO
from os import path, remove

from PIL import Image
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import Picture


def get_temporary_text_file():
    io = StringIO()
    io.write('foo')
    text_file = InMemoryUploadedFile(io, None, 'test.txt', 'text', None , None)
    text_file.seek(0)
    return text_file


def get_temporary_image():
    io = BytesIO()
    size = (200,200)
    color = (255,0,0,0)
    image = Image.new("RGBA", size, color)
    image.save(io, format='JPEG')
    image_file = InMemoryUploadedFile(io, None, 'test.jpg', 'jpeg', None, None)
    image_file.seek(0)
    return image_file


class PictureFormTests(TestCase):
    def test_if_form_submits_on_image_file(self):
        test_image = get_temporary_image()
        response = self.client.post(reverse('crop_view'), {'file': test_image, 'x': 1, 'y': 1, 'height': 10, 'width': 10})
        self.assertEqual(302, response.status_code)
        remove(path.join(path.join(settings.BASE_DIR, 'media'),test_image.name))

    def test_if_form_fails_on_text_file(self):
        test_file = get_temporary_text_file()
        response = self.client.post(reverse('crop_view'), {'file': test_file, 'x': 1, 'y': 1, 'height': 10, 'width': 10})
        self.assertEqual(200, response.status_code)

    def test_if_form_fails_on_x_value(self):
        test_image = get_temporary_image()
        response = self.client.post(reverse('crop_view'), {'file': test_image, 'x': 'abc', 'y': 1, 'height': 10, 'width': 10})
        self.assertEqual(200, response.status_code)

    def test_if_form_fails_on_y_value(self):
        test_image = get_temporary_image()
        response = self.client.post(reverse('crop_view'), {'file': test_image, 'x': 1, 'y': 'abc', 'height': 10, 'width': 10})
        self.assertEqual(200, response.status_code)
        
    def test_if_form_fails_on_height_value(self):
        test_image = get_temporary_image()
        response = self.client.post(reverse('crop_view'), {'file': test_image, 'x': 1, 'y': 1, 'height': 'abc', 'width': 10})
        self.assertEqual(200, response.status_code)

    def test_if_form_fails_on_width_value(self):
        test_image = get_temporary_image()
        response = self.client.post(reverse('crop_view'), {'file': test_image, 'x': 1, 'y': 1, 'height': 10, 'width': 'abc'})
        self.assertEqual(200, response.status_code)

    def test_model_image_field(self):
        test_image = get_temporary_image()
        Picture.objects.create(file=test_image).save()
        self.assertEqual(len(Picture.objects.all()), 1)

    def test_crop_image_url(self):
        response = self.client.get(reverse('crop_view'))
        self.assertEqual(200, response.status_code)
