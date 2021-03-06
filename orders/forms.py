from django import forms


class OrderCreateForm(forms.Form):
    """Форма оформления заказа"""
    customer_email = forms.EmailField(label='',
                                      required=True,
                                      widget=forms.EmailInput(
                                          attrs={'placeholder': 'E-mail',
                                                 'class': 'input_email'}))
