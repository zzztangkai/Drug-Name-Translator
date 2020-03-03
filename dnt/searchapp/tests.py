from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from unittest.mock import patch, MagicMock
from .views import SearchView, history_view, translate_view, more_info_view


class TestViews(TestCase):

    def test_search_view_GET(self):
        search_view = SearchView.as_view()
        search_url = reverse('search_view')
        request = RequestFactory().get(search_url)
        response = search_view(request)
        self.assertEqual(response.status_code, 200)

    @patch('searchapp.models.History.save', MagicMock(name="save"))
    def test_search_view_POST(self):
        search_view = SearchView.as_view()
        search_url = reverse('search_view')
        request = RequestFactory().post(search_url, {'search_term': 'aspirin'})
        response = search_view(request)
        self.assertEqual(response.status_code, 200)

    def test_translate_view(self):
        translate_url = reverse('translate_view')
        request = RequestFactory().get(translate_url)
        response = translate_view(request)
        self.assertEqual(response.status_code, 200)

    def test_history_view(self):
        history_url = reverse('history_view', args={'search_term': 'aspirin'})
        request = RequestFactory().get(history_url)
        response = history_view(request)
        self.assertEqual(response.status_code, 200)

    def test_more_info_view(self):
        more_info_url = reverse('more_info_view', args={'search_term': 'aspirin'})
        request = RequestFactory().get(more_info_url)
        response = more_info_view(request)
        self.assertEqual(response.status_code, 302)
