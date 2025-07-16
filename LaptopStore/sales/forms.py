from django import forms
from .models import Sale, Laptop

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer_name', 'quantity']

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError("Quantity must be a positive number.")
        return quantity

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

class LaptopForm(forms.ModelForm):
    class Meta:
        model = Laptop
        fields = ['brand', 'model', 'description', 'price', 'stock', 'image']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            max_size = 5 * 1024 * 1024  # 5MB
            if image.size > max_size:
                raise forms.ValidationError("Image file size cannot exceed 5MB.")
            return image
        return None
