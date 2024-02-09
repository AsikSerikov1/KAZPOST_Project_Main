from django import forms


class ProductForm(forms.Form):
    image = forms.ImageField()
    name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    manufacturer = forms.CharField(max_length=100)
    warranty = forms.CharField(max_length=100)
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    category_id = forms.IntegerField(required=True, min_value=1)


