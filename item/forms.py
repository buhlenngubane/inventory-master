from django import forms
from django.forms import ModelForm, ValidationError
from .models import Item



class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = [
        "item_id",
        "name",
        "item_num",
        "fragile",
        "weight",
        'units',
        "item_class",
        'item_site',
        ]

    def clean(self):
        #cleaned_data = super(Item, self).clean()
        item_site = self.cleaned_data.get("item_site")
        #food = self.cleaned_data.get("food")
        if item_site.name == "YARD": # Might not work, but this is the general idea
            #print("Bad requestsssssss")
            
            self.add_error("item_site",ValidationError("Cannot add to YARD"))
            raise ValidationError("Chocolate can't be selected with Dogs")