from django.shortcuts import render, redirect, get_object_or_404
from django.http import request
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .models import Product, Category, ProductImage
from .forms import ProductForm, ProductImageForm
from django.db.models import Q
from .models import CartItem, FavoriteItem
from django.forms import modelformset_factory


class ProductListView(ListView):
    model = Product
    template_name = 'market/product_list.html'
    context_object_name = 'products'


class ProductCreateView(CreateView):
    model = Product
    template_name = 'market/product_form.html'
    fields = ['name', 'description', 'image', 'price']
    success_url = reverse_lazy('market:product_list')


def index(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        return render(request, 'main_page.html')


def main_page(request):
    category_id = request.GET.get('category_id', None)
    categories = Category.objects.all()
    if category_id:
        products = Product.objects.filter(category_id=category_id).order_by('-created_at')
    else:
        products = Product.objects.all().order_by('-created_at')
    return render(request, 'main_page.html', {'products': products, 'categories': categories})



def account(request):
    user = request.user
    return render(request, 'account.html', {'user': user})


def upload_product(request):
    categories = Category.objects.all()
    ImageFormSet = modelformset_factory(ProductImage, form=ProductImageForm, extra=5)

    if request.method == 'POST':
        form = ProductForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES)

        category_id = request.POST.get('category')
        category = None

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            pass

        if category:
            if form.is_valid() and formset.is_valid():
                new_product = form.save(commit=False)
                new_product.category = category
                new_product.save()

                for form in formset.cleaned_data:
                    image = form.get('image')
                    if image:
                        ProductImage.objects.create(product=new_product, image=image)

                return redirect(reverse_lazy('main_page'))
        else:
            return render(request, 'upload_product.html', {'form': form, 'formset': formset, 'categories': categories, 'error_message': 'No categories found. Please add categories first.'})
    else:
        form = ProductForm()
        formset = ImageFormSet(queryset=ProductImage.objects.none())

    return render(request, 'upload_product.html', {'form': form, 'formset': formset, 'categories': categories})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    images = ProductImage.objects.filter(product=product)
    return render(request, 'product_detail.html', {'product': product, 'images': images})


def search_product(request):
    query = request.GET.get('q')
    results = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    )
    return render(request, 'search_results.html', {'results': results, 'query': query})


def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1

    cart_item.save()

    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'cart.html', {'cart_items': cart_items})


def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(pk=cart_item_id)
    if cart_item.user == request.user:
        cart_item.delete()
    return redirect('cart_view')


def add_to_favorite(request, product_id):
    product = Product.objects.get(pk=product_id)
    favorite_item, created = FavoriteItem.objects.get_or_create(user=request.user, product=product)
    return redirect('favorite_view')


def remove_from_favorite(request, favorite_item_id):
    favorite_item = FavoriteItem.objects.get(pk=favorite_item_id)
    if favorite_item.user == request.user:
        favorite_item.delete()
    return redirect('favorite_view')


def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'cart.html', {'cart_items': cart_items})


def favorite_view(request):
    favorite_items = FavoriteItem.objects.filter(user=request.user)
    return render(request, 'favorites.html', {'favorite_items': favorite_items})