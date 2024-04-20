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


class StoreCreateView(LoginRequiredMixin, CreateView):
    model = Store
    fields = ['name', 'site_users']
    template_name = "store/create.html"
    success_url = reverse_lazy('store:create')

    def form_valid(self, form):
        form.instance.manager = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        employee = Employee.objects.get(username=self.request.user.username)
        context = super(StoreCreateView, self).get_context_data(**kwargs)
        context["object_list"] = self.model.objects.filter(
            site_users=employee)
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
        context["object_list"] = self.model.objects.filter(
            site_users=employee)
        # print(pk_url_kwarg)
        return context

class StoreDetailView(LoginRequiredMixin, DetailView):
    model = Store
    template_name = "store/store_details.html"

    # def form_valid(self, form):
    #     form.instance.manager = self.request.user
    #     return super().form_valid(form)

    def get_context_data(self, **kwargs):
        employee = Employee.objects.get(username=self.request.user.username)
        context = super(StoreDetailView, self).get_context_data(**kwargs)
        context["object_list"] = self.model.objects.filter(
            site_users=employee)
        return context


class StoreDeleteView(LoginRequiredMixin, AjaxableFormMixin, DeleteView):
    model = Store
    success_url = reverse_lazy('store:list')
