from os import listdir
from os.path import splitext
from pathlib import Path

import requests
from PIL import Image
from defusedxml import ElementTree
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from pytesseract import image_to_string

from cropapp.forms import PictureForm
from login.models import User
from searchapp.forms import SearchForm
from .models import History, TranslationModel, UserHistory
from .spell import bayesClassifier


def more_info_view(request, search_term='aspirin'):
    return redirect('https://www.google.com.au/search?q=' + search_term)


def link_display_view(request, filename, link):
    user = User.objects.filter(name=request.session['user_name'])[0]
    translation_list = TranslationModel.objects.filter(image_file=filename)
    list_of_translated_drug_name = translation_list[0].translation
    list_of_translated_drug_name = list_of_translated_drug_name.split(',')
    del list_of_translated_drug_name[-1]  # delete the last element which is empty

    current_working_directory = Path.cwd()
    media_folder_path = current_working_directory.joinpath('media')
    list_of_files_in_media_folder = listdir(str(media_folder_path))

    search_term = link
    img_path = ''
    for f in list_of_files_in_media_folder:
        base_filename, _ = splitext(f)
        if base_filename == filename:
            img_file = media_folder_path.joinpath(f)
            img_path = "/media/" + str(f)
            img = Image.open(img_file)
            img.close()

    template_name = 'searchapp/search.html'
    form = SearchForm()
    form2 = PictureForm()

    form.fields['post'].initial = search_term
    list_of_drug_data = list()
    if search_term != '':
        list_of_drug_data = get_search_data(search_term)

    patient_id = 1000
    result = ''
    if list_of_drug_data is not None:
        results_found = len(list_of_drug_data)
    else:
        result = bayesClassifier(search_term)
        if result != search_term:
            results_found = 'Did you mean: '
        else:
            results_found = 'No results found!'

    list_of_searches = list()
    history_list = UserHistory.objects.filter(user=user)

    for user_history_item in history_list:
        if user_history_item is not None:
            list_of_searches.append(user_history_item.user_history)

    return render(request, template_name,
                  {'form': form, 'form2': form2, 'list_of_drug_data': list_of_drug_data, 'results_found': results_found,
                   'result': result, 'translation': list_of_translated_drug_name, 'list_of_searches': list_of_searches,
                   'img_path': img_path, 'filename': filename})


def did_you_mean_view(request, link):
    user = User.objects.filter(name=request.session['user_name'])[0]
    search_term = link
    template_name = 'searchapp/search.html'
    form = SearchForm()

    form.fields['post'].initial = search_term
    list_of_drug_data = list()
    if search_term != '':
        list_of_drug_data = get_search_data(search_term)

    patient_id = 1000
    result = ''
    if list_of_drug_data is not None:
        results_found = len(list_of_drug_data)
    else:
        result = bayesClassifier(search_term)
        if result != search_term:
            results_found = 'Did you mean: '
        else:
            results_found = 'No results found!'

    list_of_searches = list()
    history_list = UserHistory.objects.filter(user=user)

    for user_history_item in history_list:
        if user_history_item is not None:
            list_of_searches.append(user_history_item.user_history)

    return render(request, template_name,
                  {'form': form, 'list_of_drug_data': list_of_drug_data, 'results_found': results_found,
                   'result': result, 'list_of_searches': list_of_searches})


def translate_view(request, filename):
    if not request.session.get('is_login', None):
        return redirect("login")

    user = User.objects.filter(name=request.session['user_name'])[0]
    letters = [' ', '-', '_', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
               's', 't',
               'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
               'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    current_working_directory = Path.cwd()
    media_folder_path = current_working_directory.joinpath('media')
    list_of_files_in_media_folder = listdir(str(media_folder_path))
    list_of_translated_drug_name = list()
    search_term = ''
    img_path = ''

    for f in list_of_files_in_media_folder:
        base_filename, _ = splitext(f)
        if base_filename == filename:
            img_file = media_folder_path.joinpath(f)
            img_path = "/media/" + str(f)
            img = Image.open(img_file)
            text = image_to_string(img)
            text_lines = text.split('\n')

            for line in text_lines:
                if len(line) > 0:
                    line_copy = line
                    for letter in line:
                        if letter not in letters:
                            line_copy = line_copy.replace(letter, '')

                    d_name = line_copy.split(' ')[0]
                    if len(d_name) > 0:
                        list_of_translated_drug_name.append(d_name)
            if len(list_of_translated_drug_name) > 0:
                translations = ''
                for translation in list_of_translated_drug_name:
                    translations += translation + ','

                try:
                    translation_model = TranslationModel()
                    translation_model.image_file = filename
                    translation_model.translation = translations
                    translation_model.save()
                except IntegrityError:
                    TranslationModel.objects.filter(image_file=filename).delete()
                    translation_model = TranslationModel()
                    translation_model.image_file = filename
                    translation_model.translation = translations
                    translation_model.save()

                search_term = list_of_translated_drug_name[0]
            img.close()

    template_name = 'searchapp/search.html'
    form = SearchForm()
    form2 = PictureForm()

    form.fields['post'].initial = search_term
    list_of_drug_data = list()
    if search_term != '':
        list_of_drug_data = get_search_data(search_term)

    patient_id = 1000
    result = ''
    if list_of_drug_data is not None:
        results_found = len(list_of_drug_data)
    else:
        result = bayesClassifier(search_term)
        if result != search_term:
            results_found = ' Did you mean: '
        else:
            results_found = 'No results found!'

    list_of_searches = list()
    history_list = UserHistory.objects.filter(user=user)

    for user_history_item in history_list:
        if user_history_item is not None:
            list_of_searches.append(user_history_item.user_history)

    return render(request, template_name,
                  {'form': form, 'form2': form2, 'list_of_drug_data': list_of_drug_data, 'results_found': results_found,
                   'result': result, 'translation': list_of_translated_drug_name, 'list_of_searches': list_of_searches,
                   'img_path': img_path, 'filename': filename})


def history_view(request, history_term='aspirin'):
    if not request.session.get('is_login', None):
        return redirect("login")

    user = User.objects.filter(name=request.session['user_name'])[0]
    template_name = 'searchapp/search.html'
    form = SearchForm()
    form2 = PictureForm()
    form.fields['post'].initial = history_term

    result = ''
    patient_id = 1000
    search_term = history_term
    list_of_drug_data = get_search_data(search_term)
    if list_of_drug_data is not None:
        results_found = len(list_of_drug_data)
    else:
        result = bayesClassifier(search_term)
        if result != search_term:
            results_found = ' Did you mean: '
        else:
            results_found = 'No results found!'

    list_of_searches = list()

    history_list = UserHistory.objects.filter(user=user)

    for user_history_item in history_list:
        if user_history_item is not None:
            list_of_searches.append(user_history_item.user_history)

    return render(request, template_name,
                  {'form': form, 'form2': form2, 'list_of_drug_data': list_of_drug_data, 'results_found': results_found,
                   'result': result, 'translation': '', 'list_of_searches': list_of_searches})


def get_search_data(search_term):
    list_of_drug_data = list()
    if search_term is not None:
        request_url = 'https://api.pbs.gov.au/0.3/search.xml?term=' + search_term + '&effectivedate=2019-07-01&view' \
                                                                                    '=item&api_key' \
                                                                                    '=a643d03c2152a311e37f8e4a7afd43e6 '
        response = requests.get(request_url)
        if response.status_code == 200:
            xml_response = response.text[38:]  # Remove first <?xml...?> tag that confuses the parser
            items = ElementTree.fromstring(xml_response)  # Build the xml tree with root element being items
            for item in items:  # Traverse each tag that is the direct child of 'items'
                drug_data = {}
                for child_of_item in item:  # Traverse each tag that is the direct child of 'item'
                    if child_of_item.tag[27:] in 'GenericDrug.Name':  # if we get to the tag of 'GenericDrug.Name'
                        drug_data['generic_name'] = child_of_item.text

                    if child_of_item.tag[27:] in 'Brands':  # if we get to the tag of 'Brands'
                        list_of_brands = list()
                        for child_of_brands in child_of_item:  # Traverse each tag that is the direct child of 'Brands'
                            brand = {}
                            for child_of_brand in child_of_brands:  # Traverse each tag that is the direct child of
                                # 'Brand'
                                if child_of_brand.tag[27:] in 'Brand.Name':  # if we get to the tag of 'Brand.Name'
                                    brand['brand_name'] = child_of_brand.text

                                elif child_of_brand.tag[27:] in 'Item.FormStrengthLI':  # if we get to the
                                    # tag of 'Item.FormStrengthLI'
                                    brand['description'] = child_of_brand.text

                                elif child_of_brand.tag[27:] in 'Item.PackFormStrength':  # if we get to the tag of
                                    # 'Item.PackFormStrength'
                                    brand['reaction'] = child_of_brand.text

                                elif child_of_brand.tag[27:] in 'Manufacturer.Name':  # if we get to the
                                    # tag of 'Manufacturer.Name'
                                    brand['manufacturer'] = child_of_brand.text

                                elif child_of_brand.tag[27:] in 'Price.PriceToConsumer':  # if we get to the
                                    # tag of consumer price
                                    brand['price'] = child_of_brand.text
                                    list_of_brands.append(brand)
                        drug_data['brands'] = list_of_brands
                list_of_drug_data.append(drug_data)
            return list_of_drug_data
        else:
            return None


def clear_history_view(request):
    user = User.objects.filter(name=request.session['user_name'])[0]
    UserHistory.objects.filter(user=user).delete()

    return redirect('search_view')


class SearchView(TemplateView):
    template_name = 'searchapp/search.html'

    def get(self, request):
        if not request.session.get('is_login', None):
            return redirect("login")

        form2 = PictureForm()
        form = SearchForm()
        patient_id = 1000
        list_of_drug_data = list()
        list_of_searches = list()

        user = User.objects.filter(name=request.session['user_name'])[0]
        history_list = UserHistory.objects.filter(user=user)

        for history_item in history_list:
            if history_item is not None:
                list_of_searches.append(history_item.user_history)

        return render(request, self.template_name,
                      {'form': form, 'form2': form2, 'list_of_drug_data': list_of_drug_data, 'translation': '',
                       'list_of_searches': list_of_searches})

    def post(self, request):
        user = User.objects.filter(name=request.session['user_name'])[0]  # Logged in user instance
        form = SearchForm(request.POST)
        form2 = PictureForm()
        patient_id = 1000
        search_term = request.POST.get('post')
        search_term_found = False

        history_list = UserHistory.objects.filter(user=user)
        for user_history_item in history_list:
            if user_history_item is not None:
                history_item = user_history_item.user_history
                if search_term == history_item.search_term:
                    search_term_found = True
                    break

        search_term_clean = search_term
        if not search_term_found:
            letters = [' ', '-', '_', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                       'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                       'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1',
                       '2', '3', '4', '5', '6', '7', '8', '9']

            for letter in search_term:
                if letter not in letters:
                    search_term_clean = search_term_clean.replace(letter, '')
            if len(search_term_clean) > 0:
                history = History(search_term=search_term_clean)
                history.save()
                user_history_model = UserHistory(user=user, user_history=history)
                user_history_model.save()

        result = ''
        list_of_drug_data = get_search_data(search_term_clean)
        if list_of_drug_data is not None:
            results_found = len(list_of_drug_data)
        else:
            result = bayesClassifier(search_term)
            if result != search_term:
                results_found = 'Did you mean: '
            else:
                results_found = 'No results found!'

        list_of_searches = list()
        history_list = UserHistory.objects.filter(user=user)

        for user_history_item in history_list:
            if user_history_item is not None:
                history_item = user_history_item.user_history
                list_of_searches.append(history_item)

        return render(request, self.template_name,
                      {'form': form, 'form2': form2, 'list_of_drug_data': list_of_drug_data,
                       'results_found': results_found, 'result': result, 'translation': '', 'list_of_searches': list_of_searches})
