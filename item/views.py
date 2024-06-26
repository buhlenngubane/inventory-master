from django.forms import BaseModelForm
from django.http import HttpResponse
from item.forms import ItemForm
from mixins import AjaxableFormMixin
from django.template import RequestContext
from django.views.generic import (
    CreateView,
    DetailView,
    DeleteView,
    ListView,
    UpdateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from .models import Item
from accounts.models import Employee
from store.models import Store
# Create your views here.


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    fields = []
    template_name = "item/update_item.html"
    success_url = reverse_lazy('item:index')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        item = self.object
        print(item)
        item.item_site = Store.objects.get(name="YARD")
        messages.success(self.request,"Item added to YARD")
        return super().form_valid(form)


class ItemDeleteView(LoginRequiredMixin,AjaxableFormMixin, DeleteView):
    model = Item
    
    success_url = reverse_lazy('item:index')

    def form_valid(self, form):
        # print(self.model.objects.values())
        site = self.object.item_site
        store = Store.objects.get(
                name=site.name).number_of_items
        Store.objects.filter(name=site.name).update(number_of_items=store -
                                                                   self.object.item_num)
        messages.success(self.request,"Item successfully removed")
        return super().form_valid(form)


class ListAndCreate(LoginRequiredMixin, AjaxableFormMixin, CreateView):
    form_class=ItemForm
    model = Item
    '''fields = [
        "item_id",
        "name",
        "item_num",
        "fragile",
        "weight",
        'units',
        "item_class",
        'item_site',
    ]'''
    template_name = "item/create.html"
    success_url = reverse_lazy('item:index')
    
    def form_invalid(self, form):
        print("Form invalid")
        messages.error(self.request,"You cannot edit YARD")
        #reverse_lazy('item:index')
        #self.get_form(form).fields.clear()
        return super().form_invalid(form)

    def form_valid(self, form):
        print(form.instance.item_site)
        form.instance.added_by = self.request.user
        store = Store.objects.get(
            name=form.instance.item_site).number_of_items
        yard_items = Store.objects.get(
            name="YARD").number_of_items
        if form.instance.item_site.name == "YARD":
            print("Trying to add to yard")
            
            Store.objects.filter(name="YARD").update(number_of_items=yard_items +
                                                                   form.instance.item_num)
            #return super().get_permission_denied_message()
        else:
            site = Store.objects.get(name="YARD")
            item_to_del = Item.objects.get(item_site = site, name = form.instance.name)
            print(item_to_del)
            items = item_to_del.item_num - form.instance.item_num
            if items > 0:
                item_to_del.item_num = items
                item_to_del.save()
                Store.objects.filter(name=form.instance.item_site).update(number_of_items=store +
                                                                   form.instance.item_num)
                Store.objects.filter(name="YARD").update(number_of_items=yard_items -
                                                                   form.instance.item_num)
            elif items == 0:
                item_to_del.delete()
                Store.objects.filter(name=form.instance.item_site).update(number_of_items=store +
                                                                   form.instance.item_num)
                Store.objects.filter(name="YARD").update(number_of_items=yard_items -
                                                                   form.instance.item_num)                

       
        #Store.objects.get().update(num)
        

        
        messages.success(self.request,"Item successfully added")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        employee = Employee.objects.get(username=self.request.user.username)
        context = super(ListAndCreate, self).get_context_data(**kwargs)
        context["object_list"] = self.model.objects.filter(added_by=employee)
        context['Total'] = 0
        print()
        for item in context["object_list"]:
            context['Total'] += item.item_num
        return context


class ListAndDetail(LoginRequiredMixin, DetailView):
    model = Item
    template_name = "item/item.html"

    def get_context_data(self, **kwargs):
        employee = Employee.objects.get(username=self.request.user.username)
        # site = Store.objects.get(name=)
        context = super(ListAndDetail, self).get_context_data(**kwargs)
        context["object_list"] = self.model.objects.filter(added_by=employee)
        

        return context


class ItemSearchView(LoginRequiredMixin, ListView):
    model = Item
    template_name = "item/create.html"

    def get_context_data(self, **kwargs):
        query = self.request.GET.get('query')
        employee = Employee.objects.get(username=self.request.user.username)
        context = super(ItemSearchView, self).get_context_data(**kwargs)
        context["object_list"] = self.model.objects.filter(
            #Q(added_by=employee) & 
            (Q(name__icontains=query) | Q(item_id__icontains=query)))
        return context
