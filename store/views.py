from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.views.generic import (
    CreateView,
    DetailView,
    DeleteView,
    # UpdateView,
    ListView)
from django.views.generic.edit import UpdateView
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from item.models import Item
from mixins import AjaxableFormMixin
from .models import Store
from accounts.models import Employee
from django import template
from django.contrib import messages
from django.shortcuts import render, redirect

register = template.Library()

# @register.filter
# def replace(value, arg):
#     """
#     Replacing filter
#     Use `{{ "aaa"|replace:"a|b" }}`
#     """
#     if len(arg.split('|')) != 2:
#         return value

#     what, to = arg.split('|')
#     return value.replace(what, to)

# Create your views here.

class StoreListView(LoginRequiredMixin, ListView):
    model = Store
    success_url = reverse_lazy('store:list')
    def demo_piechart(self, **kwargs):
        """
        pieChart page
        """
        stores = Store.objects.all()
        store = stores.get(store_id = kwargs['pk'])
        items = Item.objects.filter(item_site = store)
        
        xdata = [item.name for item in items]#["Apple", "Apricot", "Avocado", "Banana", "Boysenberries", "Blueberries", "Dates", "Grapefruit", "Kiwi", "Lemon"]
        ydata = [item.item_num for item in items]#[52, 48, 160, 94, 75, 71, 490, 82, 46, 17]
        

        extra_serie = {"tooltip": {"y_start": "", "y_end": " cal"}}
        chartdata = {'x': xdata, 'y1': ydata, 'extra1': extra_serie}
        charttype = "pieChart"

        chartcontainer = 'piechart_container'
        data = {
            'charttype': charttype,
            'chartdata': chartdata,
            "chartcontainer":chartcontainer,
            'extra': {
                'x_is_date': False,
                'x_axis_format': '',
                'tag_script_js': True,
                'jquery_on_ready': True,
            },
            'object_list': stores,
            'object': store
        }
        print(items)
        #context = super(StoreListView, self).get_context_data(**kwargs)
        return render(self,'store/store_piechart.html', data)
    
    def get_context_data(self, **kwargs):
        employee = Employee.objects.get(username=self.request.user.username)
        # pk_url_kwarg = self.kwargs['pk']
        context = super(StoreListView, self).get_context_data(**kwargs)
        context["object_list"] = self.model.objects.values_list(["store_id","name", "site_users"])
        # print(pk_url_kwarg)
        return context



class StoreCreateView(LoginRequiredMixin, CreateView):
    model = Store
    fields = ['name', 'site_users']
    template_name = "store/create.html"
    success_url = reverse_lazy('store:create')

    def form_valid(self, form):
        form.instance.manager = self.request.user
        messages.success(self.request, 'Form submission successful')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        employee = Employee.objects.get(username=self.request.user.username)
        context = super(StoreCreateView, self).get_context_data(**kwargs)
        context["object_list"] = self.model.objects.all()#.values(["store_id","name", "site_users"])
        print("Object list",context["object_list"])
        return context

class StoreUpdateView(LoginRequiredMixin, UpdateView):
    model = Store
    #model = xxxxxxxxxx
    fields = ['name','site_users']#'__all__'
    template_name_suffix = "_update"
    # pk_url_kwarg = None
    # template_name = "store/store_update.html"
    success_url = reverse_lazy(f'store:list')
    SUCCESS	= 25

    def form_valid(self, form):
        form.instance.manager = self.request.user
        self.object.save()

        messages.success(self.request, 'Form submission successful')
        
        return HttpResponseRedirect(self.request.path_info)
    
    def get_context_data(self, **kwargs):
        employee = Employee.objects.get(username=self.request.user.username)
        # pk_url_kwarg = self.kwargs['pk']
        context = super(StoreUpdateView, self).get_context_data(**kwargs)
        context["object_list"] = self.model.objects.values_list(["store_id","name", "site_users"])
        # print(pk_url_kwarg)
        return context

class StoreDetailView(LoginRequiredMixin, DetailView):
    model = Store
    template_name = "store/store_details.html"
    # def form_valid(self, form):
    #     form.instance.manager = self.request.user
    #     return super().form_valid(form)

    

    def get_context_data(self, **kwargs):
        #employee = Employee.objects.all()
        context = super(StoreDetailView, self).get_context_data(**kwargs)
        context["object_list"] = self.model.objects.all()#.values_list(["store_id","name", "site_users"])
        print("Object list",context["object_list"])
        return context


class StoreDeleteView(LoginRequiredMixin, AjaxableFormMixin, DeleteView):
    model = Store
    success_url = reverse_lazy('store:list')

    def form_valid(self, form):
        form.instance.manager = self.request.user
        #self.object.save()

        messages.success(self.request, f'You havr deleted {self.object.name}')
        
        return HttpResponseRedirect(self.request.path_info)
