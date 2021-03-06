from django import forms


class ProductFilterForm(forms.Form):
    """Форма сортировки товаров"""
    ordering = forms.ChoiceField(label='',
                                 required=False,
                                 initial='name',
                                 choices=[
                                     ['name', 'По имени'],
                                     ['price', 'По возрастанию цены'],
                                     ['-price', 'По убыванию цены'],
                                 ])
