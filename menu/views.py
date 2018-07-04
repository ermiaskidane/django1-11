from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from .models import Item
from .forms import ItemForm
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView

# Create your views here.
class HomeView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return render(request, 'home.html', {})

        user = request.user
        is_following_user_ids = [x.user.id for x in user.is_following.all()]
        # list_
        # for x in user.is_following.all():
        #     list_.append(x.user.id)
        """getting the user items """
        rl = Item.objects.filter(user__id__in=is_following_user_ids, public=True).order_by('-updated')[:3]
        # return render(request, 'menu/home-feed.html', {'rl':rl})  swop rl to object_list for matchin perpose in home-feed.html
        return render(request, 'menu/home-feed.html', {'object_list':rl})


class ItemListView(LoginRequiredMixin, ListView):
    # queryset = Item.objects.all()
    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)

# COMBINE WITH THE ITEMUPDATEVIEW
class ItemDetailView(LoginRequiredMixin, DetailView):
    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)


class ItemCreateView(LoginRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = ItemForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        return super(ItemCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(ItemCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        # kwargs['instance'] = Item.objects.filter(user=self.request.user).first()
        # print(kwargs)
        return kwargs

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(ItemCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = "Create Item"
        return context


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    # template_name = 'form.html'
    template_name = 'menu/detail-update.html'
    form_class = ItemForm

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(ItemUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = "Update Item"
        return context

    def get_form_kwargs(self):
        print(self.kwargs)
        kwargs = super(ItemUpdateView, self).get_form_kwargs()
        print(kwargs)
        kwargs['user'] = self.request.user
        print(kwargs['user'])
        # kwargs['instance'] = Item.objects.filter(user=self.request.user).first()
        # print(kwargs)
        return kwargs
