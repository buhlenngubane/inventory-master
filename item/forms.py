from django import forms
from django.forms import ModelForm, ValidationError
from django.contrib import messages
from store.models import Store
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
        item_name = self.cleaned_data.get("name")
        item_units = self.cleaned_data.get("item_num")
        #food = self.cleaned_data.get("food")
        if item_site.name != "YARD": # Might not work, but this is the general idea
            #print("Bad requestsssssss")
            site = Store.objects.get(name="YARD")
            item_to_del = Item.objects.get(item_site = site, name = item_name)
            print(item_to_del)
            if item_units > item_to_del.item_num:
                self.add_error("item_site",ValidationError("The Item is not available in YARD"))
                messages.error(self.request,"The Item is not available in YARD")
                raise ValidationError("The Item is not available in YARD")