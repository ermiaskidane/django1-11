from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, View

from restaurant.models import RestaurantLocation
from menu.models import Item

from .forms import RegisterForm
from .models import Profile

User = get_user_model()
# Create your views here.

def activate_user_view(request, code=None, *args, **kwargs):
    print(code)  #it is just the activation_key , for some reason args and kwargs are empty
    # print(kwargs)
    if code:
        rl = Profile.objects.filter(activation_key=code)
        if rl.exists() and rl.count() == 1:
            profile = rl.first()
            if not profile.activated:
                user_ = profile.user
                user_.is_active = True
                user_.save()
                profile.activated = True
                profile.activation_key = None # or False
                profile.save()
                return redirect("/login")     # or HttpResponseRedirect("/login")
    # invalid code
    return redirect("/login") # or HttpResponseRedirect("/login")

class RegisterView(CreateView):   ##url is on root url
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = '/'

    # if the user is already authenticated it will use this method
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return redirect ("/logout")
        return super(RegisterView,self).dispatch(*args, **kwargs)


class ProfileFollowToggle(LoginRequiredMixin, View):    #the url for this on main app

    def post(self, request, *args, **kwargs):
        # print(request.data)
        print(request.POST)
        username_to_toggle = request.POST.get('username') # way of checking if the user is authenticated
        profile_, is_following = Profile.objects.toggle_follow(request.user, username_to_toggle)
        print(is_following)
        # print(username_to_toggle)
        # profile_= Profile.objects.get(user__username__iexact=username_to_toggle)
        # user = request.user
        # if user in profile_.followers.all():
        #     profile_.followers.remove(user)
        # else:
        #     profile_.followers.add(user)
        # return redirect('/u/eri/')
        return redirect(f'/u/{profile_.user.username}/')

class ProfileDetailView(DetailView):
    # queryset = User.objects.all()
    # queryset = User.objects.filter(is_active=True)  #no needed, am getting the query using the get_object function
    template_name = 'profiles/user.html'

    def get_object(self):
        # username = self.kwargs.get('username', None)
        # print(self.kwargs)    #{'username': 'ermias'}
        username = self.kwargs.get('username')
        if username is None:
            raise Http404
        # print(username)
        return get_object_or_404(User, username__iexact=username, is_active=True)


    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProfileDetailView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     # user = self.get_object()
    #     user = context['user']
    #     query = self.request.GET.get('q')
    #     items_exists = Item.objects.filter(user=user).exists()
    #     rl = RestaurantLocation.objects.filter(owner=user)
    #     if query:
    #         # rl = rl.filter(location__icontains=query)
    #         rl = rl.filter(name__icontains=query)
    #
    #     if items_exists and rl.exists() :
    #         context['locations'] = rl
    #     return context

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(*args, **kwargs)
        # print(context)
        # user = self.get_object()
        user = context['user']
        # is_following = False
        # if user.profile in self.request.user.is_following.all():
        #     is_following = True
        # context['is_following'] = is_following
        query = self.request.GET.get('q')
        items_exists = Item.objects.filter(user=user).exists()
        rl = RestaurantLocation.objects.filter(owner=user).search(query)
        # if query:
        #     rl = rl.search(query)
        #     # rl = RestaurantLocation.objects.search(query)
        if items_exists and rl.exists() :
            context['locations'] = rl
        return context
