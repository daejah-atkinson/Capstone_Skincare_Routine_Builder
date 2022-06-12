from django.shortcuts import render
from django.views import View 
from django.http import HttpResponse 
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from .models import Product, Brand, Routine, Favorite 
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class Home(TemplateView):
    template_name = "routines.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["routines"] = Routine.objects.all()
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")
        if name != None:
            context["routines"] = Routine.objects.filter(
                name__icontains=name, user=self.request.user)
        else:
            context["routines"] = Routine.objects.filter(user=self.request.user)
        return context

class About(TemplateView):
    template_name = "about.html"

@method_decorator(login_required, name='dispatch')
class ProductList(TemplateView):
    template_name = "product_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.all() 
        return context
    

@method_decorator(login_required, name='dispatch')
class ProductDetail(DetailView):
    model = Product
    template_name = "product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")
        if name != None:
            context["brands"] = Brand.objects.filter(
                name__icontains=name, user=self.request.user)
        else:
            context["brands"] = Brand.objects.filter(user=self.request.user)
        return context


@method_decorator(login_required, name='dispatch')
class BrandCreate(View):

    def post(self, request, pk):
        brand = request.POST.get("brand")
        name = request.POST.get("name")
        img = request.POST.get("img")
        link = request.POST.get("link")
        product = Product.objects.get(pk=pk)
        Brand.objects.create(brand=brand, name=name, img=img, link=link, product=product)
        return redirect('product_detail', pk=pk)
    
    def form_valid(self,form):
        form.instance.user = self.request.user
        return super(BrandCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")
        if name != None:
            context["brands"] = Brand.objects.filter(
                name__icontains=name, user=self.request.user)
        else:
            context["brands"] = Brand.objects.filter(user=self.request.user)
        return context

@method_decorator(login_required, name='dispatch')
class FavoriteCreate(View):

    def post(self, request, pk):
        brand = Brand.objects.get(pk=pk)
        Favorite.objects.create(brand=brand)
        return redirect('favorites')
    
    def form_valid(self,form):
        form.instance.user = self.request.user
        return super(FavoriteCreate, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class BrandDetail(DetailView):
    model = Brand
    template_name = "brand_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["favorites"] = Favorite.objects.all()
        context["routines"] = Routine.objects.all()
        return context

class BrandUpdate(UpdateView):
    model = Brand
    fields = ['brand', 'name', 'img', 'link']
    template_name = 'brand_update.html'
    success_url = '/products/'

    def get_success_url(self):
        return reverse('brand_detail', kwargs={'pk': self.object.pk})

@method_decorator(login_required, name='dispatch')
class RoutineBrandAssoc(View):

    def get(self, request, pk, brand_pk):
        assoc = request.GET.get("assoc")
        if assoc == "remove":
            Routine.objects.get(pk=pk).brands.remove(brand_pk)
        if assoc == "add":
            Routine.objects.get(pk=pk).brands.add(brand_pk)
        return redirect('home')


@method_decorator(login_required, name='dispatch')
class FavoriteProduct(TemplateView):
    template_name = "favorites.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["favorites"] = Favorite.objects.all()
        return context
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")
        if name != None:
            context["favorites"] = Favorite.objects.filter(
                name__icontains=name, user=self.request.user)
        else:
            context["favorites"] = Favorite.objects.filter(user=self.request.user)
        return context

@method_decorator(login_required, name='dispatch')
class FavoriteBrandAssoc(View):

    def get(self, request, pk, brand_pk):
        assoc = request.GET.get("assoc")
        if assoc == "remove":
            Favorite.objects.get(pk=pk).brands.remove(brand_pk)
        if assoc == "add":
            Favorite.objects.get(pk=pk).brands.add(brand_pk)
        return redirect('favorites')

class Signup(View):
    def get(self, request):
        form = UserCreationForm()
        context = {"form": form}
        return render(request, "registration/signup.html", context)
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("product_list")
        else:
            context = {"form": form}
            return render(request, "registration/signup.html", context)
