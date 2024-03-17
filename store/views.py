from django.template import RequestContext
from django.views.generic import (
    CreateView,
    DetailView,
    DeleteView,
    ListView,
    UpdateView)
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from mixins import AjaxableFormMixin
from .models import Store
from accounts.models import Employee
from django import template

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

class StoreDetailView(LoginRequiredMixin, DetailView):
    model = Store
    template_name = "store/details.html"

    def get_context_data(self, **kwargs):
        employee = Employee.objects.get(username=self.request.user.username)
        context = super(StoreDetailView, self).get_context_data(**kwargs)
        context["object_list"] = self.model.objects.filter(
            site_users=employee)
        return context


class StoreDeleteView(LoginRequiredMixin, AjaxableFormMixin, DeleteView):
    model = Store
    success_url = reverse_lazy('store:list')
