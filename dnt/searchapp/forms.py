from django import forms


class SearchForm(forms.Form):
    post = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['id'] = 'searchterm'
            visible.field.widget.attrs['type'] = 'text'
