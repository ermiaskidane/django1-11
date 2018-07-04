from django.conf.urls import url
from .views import ( #restaurant_listview,
                            RestaurantListView,
                            # SearchRestaurantListView,
                            # AfricanRestaurantListView,
                            RestaurantDetailView,
                            # restaurant_createview,
                            RestaurantCreateView,
                            RestaurantUpdateView
                            )



urlpatterns = [
    # url(r'^restaurant/$',  restaurant_listview),
    url(r'^$',  RestaurantListView.as_view(), name="list"),
    # url(r'^restaurant/create/$',  restaurant_createview), # for the forms
    url(r'^create/$',  RestaurantCreateView.as_view(), name="create"),
    # url(r'^restaurant/(?P<slug>\w+)/$',  SearchRestaurantListView.as_view()),
    # url(r'^restaurant/(?P<rest_id>\w+)/$',  RestaurantDetailView.as_view()),
    # url(r'^(?P<slug>[\w-]+)/edit/$',  RestaurantUpdateView.as_view(), name="edit"),
    # url(r'^(?P<slug>[\w-]+)/$',  RestaurantDetailView.as_view(), name="detail"),
    url(r'^(?P<slug>[\w-]+)/$',  RestaurantUpdateView.as_view(), name="detail"),
    # url(r'^restaurant/african/$',  AfricanRestaurantListView.as_view()),
]
