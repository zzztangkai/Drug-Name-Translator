from os import remove, rename
from os.path import splitext
from django.shortcuts import render, redirect
from pathlib import Path

from .forms import PictureForm


def crop_view(request):
    if not request.session.get('is_login', None):
        return redirect("login")

    if request.method == 'POST':
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                   't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                   'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6',
                   '7', '8', '9']
        form = PictureForm(request.POST, request.FILES)

        media_folder_path = Path.joinpath(Path.cwd(), 'media')
        file_path = media_folder_path.joinpath(str(request.FILES['file']))
        filename = str(request.FILES['file'])
        base_filename, file_extension = splitext(filename)
        base_filename_copy = base_filename

        for letter in base_filename:
            if letter not in letters:
                base_filename_copy = base_filename_copy.replace(letter, '')
        filename = base_filename_copy + file_extension

        if form.is_valid():
            form.save(commit=False)
            try:
                rename(str(file_path), str(media_folder_path.joinpath(filename)))
            except FileExistsError:
                remove(str(media_folder_path.joinpath(filename)))
                rename(str(file_path), str(media_folder_path.joinpath(filename)))

            return redirect('translate_view', base_filename_copy)
    else:
        form = PictureForm()

    return render(request, 'cropapp/image_crop.html', {'form': form})
