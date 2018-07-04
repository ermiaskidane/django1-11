"""ecommerce2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from restaurant.views import ( #restaurant_listview,
                            RestaurantListView,
                            SearchRestaurantListView,
                            # AfricanRestaurantListView,
                            RestaurantDetailView,
                            # restaurant_createview,
                            RestaurantCreateView
                            )

from django.views.generic import TemplateView

# from django.contrib.auth import views as auth_views
# url(r'^accounts/login/$', auth_views.LoginView.as_view()),
from django.contrib.auth.views import LoginView , LogoutView #PasswordResetForm  url(r'^password_reset/$',PasswordResetForm, name="password_reset"),
from menu.views import HomeView

### this is from profile module
from profiles.views import ProfileFollowToggle, RegisterView, activate_user_view



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^$', TemplateView.as_view(template_name="home.html"), name="home"),
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^register/$',RegisterView.as_view(), name="register"),
    url(r'^login/$',LoginView.as_view(), name="login"),
    url(r'^logout/$',LogoutView.as_view(), name="logout"),
    url(r'^activate/(?P<code>[a-z0-9].*)/$', activate_user_view, name="activate"),
    url(r'^profile-follow/$',ProfileFollowToggle.as_view(), name="follow"),
    url(r'^u/', include('profiles.urls', namespace="profiles")),
    url(r'^items/', include('menu.urls', namespace="menu")),
    url(r'^restaurant/', include('restaurant.urls', namespace="restaurant")),
    # url(r'^restaurant/$',  restaurant_listview),
    ## url(r'^restaurant/$',  RestaurantListView.as_view(), name="restaurant"),
    # url(r'^restaurant/create/$',  restaurant_createview), # for the forms
    ## url(r'^restaurant/create/$',  RestaurantCreateView.as_view(), name="restaurant_create"),
    # url(r'^restaurant/(?P<slug>\w+)/$',  SearchRestaurantListView.as_view()),
    # url(r'^restaurant/(?P<rest_id>\w+)/$',  RestaurantDetailView.as_view()),
    ## url(r'^restaurant/(?P<slug>[\w-]+)/$',  RestaurantDetailView.as_view(), name="restaurant_detail"),
    # url(r'^restaurant/african/$',  AfricanRestaurantListView.as_view()),
    url(r'^about/$', TemplateView.as_view(template_name="about.html"), name="about"),
    url(r'^contact/$', TemplateView.as_view(template_name="contact.html"), name="contact")
]
