from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.db.models import Q

import random
from .models import RestaurantLocation
from .forms import RestaurantCreateForm, RestaurantLocationCreateForm

# Create your views here.




###### CLASS BASE VIEWS #############

# class RestaurantListView(ListView):
#     queryset = RestaurantLocation.objects.all()
#     template_name = 'restaurant/restaurant_list.html'
#
# class MexicanRestaurantListView(ListView):
#     queryset = RestaurantLocation.objects.filter(catagory__iexact="mexican")
#     template_name = 'restaurant/restaurant_list.html'
#
# class AfricanRestaurantListView(ListView):
#     queryset = RestaurantLocation.objects.filter(catagory__iexact="african")
#     template_name = 'restaurant/restaurant_list.html'

class RestaurantListView(ListView):
    # queryset = RestaurantLocation.objects.all()
    template_name = 'restaurant/restaurant_list.html'

    def get_queryset(self):
        return  RestaurantLocation.objects.filter(owner=self.request.user)

class SearchRestaurantListView(LoginRequiredMixin, ListView):
    template_name = 'restaurant/restaurant_list.html'

    # def get_queryset(self):
    #     return  RestaurantLocation.objects.filter(owner=self.request.user)

    ### make sense when we search from things
    # def get_queryset(self):
    #     print(self.kwargs)
    #     slug = self.kwargs.get('slug')
    #     if slug:
    #         queryset = RestaurantLocation.objects.filter(
    #                 Q(catagory__iexact=slug) |
    #                 Q(catagory__icontains=slug)
    #                 )
    #     else:
    #         queryset = RestaurantLocation.objects.none()  # OR queryset = RestaurantLocation.objects.all()
    #     return queryset

##### FIRST METHOD FOR FORMS ######

# def restaurant_createview(request):
#     # if request.method == "GET":
#     #     print("get data")
#     if request.method == "POST":
#         title = request.POST.get("title") #request.POST["title"]
#         location = request.POST.get("location")
#         category = request.POST.get("category")
#         # files = request.POST.get('files')
#         obj = RestaurantLocation.objects.create(
#                 name = title,
#                 location= location,
#                 category = category,
#                 # files = files
#             )
#         return HttpResponseRedirect("/restaurant/")
#     template_name = 'restaurant/form.html'
#     context = {}
#     return render(request, template_name, context)

##### SECOND METHOD  FOR FORMS ######
# def restaurant_createview(request):
#     form = RestaurantCreateForm(request.POST or None)
#     errors = None
#     # if request.method == "POST":
#     #     form = RestaurantCreateForm(request.POST)
#     if form.is_valid():
#         obj = RestaurantLocation.objects.create(
#                 name = form.cleaned_data.get('name'),
#                 location= form.cleaned_data.get('location'),
#                 category = form.cleaned_data.get('category'),
#                 # files = files
#             )
#         return HttpResponseRedirect("/restaurant/")
#     if form.errors:
#         # print(form.errors)
#         errors = form.errors
#     template_name = 'restaurant/form.html'
#     context = {'form':form, 'errors':errors}
#     return render(request, template_name, context)

##### THIRD METHOD  FOR FORMS ######
# @login_required(login_url='/login/')
# def restaurant_createview(request):
#     form = RestaurantLocationCreateForm(request.POST or None)
#     errors = None
#     if form.is_valid():
#         if request.user.is_authenticated():
#             instance = form.save(commit=False)
#             # customize
#             # like a pre_save
#             instance.owner = request.user
#             instance.save()
#             # form.save()
#             # like a post_save
#             return HttpResponseRedirect("/restaurant/")
#         else:
#             return HttpResponseRedirect('/login/')
#     if form.errors:
#         # print(form.errors)
#         errors = form.errors
#     template_name = 'restaurant/form.html'
#     context = {'form':form, 'errors':errors}
#     return render(request, template_name, context)

##### FOURTH METHOD  FOR FORMS VIA CLASS BASE VIEW (efficent) ######
class RestaurantCreateView(LoginRequiredMixin, CreateView):
    form_class = RestaurantLocationCreateForm
    # login_url = '/login/'
    # template_name = 'restaurant/form.html'
    template_name = 'form.html'
    # success_url = '/restaurant/'

    def form_valid(self, form):
        instance = form.save(commit=False)
        # customize
        # like a pre_save
        instance.owner = self.request.user
        # form.save()
        # like a post_save
        return super(RestaurantCreateView, self).form_valid(form)

    ## this queryset is for the menu app
    def get_context_data(self, *args, **kwargs):
        context = super(RestaurantCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = "Add Restaurant"
        return context

# THIS DETAIL CLASS IS COMBINED WITH UPDATEVIEW
class RestaurantDetailView(LoginRequiredMixin, DetailView):
    # queryset = RestaurantLocation.objects.all() #filter(catagory__iexact="american")
    def get_queryset(self):
        return  RestaurantLocation.objects.filter(owner=self.request.user)

class RestaurantUpdateView(LoginRequiredMixin, UpdateView):
    form_class = RestaurantLocationCreateForm
    login_url = '/login/'
    # template_name = 'restaurant/form.html'
    ## template_name = 'form.html'
    template_name = 'restaurant/detail-update.html'


    # this queryset is for the menu app
    def get_context_data(self, *args, **kwargs):
        context = super(RestaurantUpdateView, self).get_context_data(*args, **kwargs)
        name = self.get_object().name
        # context['title'] = "Update Restaurant"
        context['title'] = f'Update Restaurant: {name}'
        return context

    def get_queryset(self):
        return  RestaurantLocation.objects.filter(owner=self.request.user)
