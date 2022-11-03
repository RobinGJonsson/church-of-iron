from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.db.models.functions import Lower
from django.contrib.auth.models import User
from .models import Category, Product
from .forms import ProductForm


def store_view(request):
    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request,
                               ("You didn't enter any search criteria!"))
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(
                description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'store/store.html', context)


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)

    context = {
        'product': product,
    }

    return render(request, 'store/product_detail.html', context)


def is_store_manager(user):
    return user.groups.filter(name='Store Manager').exists()


@login_required
@user_passes_test(is_store_manager)
def edit_product(request, product_id):
    product = Product.objects.get(id=product_id)
    form = ProductForm(instance=product)

    if request.method == 'POST':
        rp = request.POST
        form = ProductForm(rp, request.FILES, instance=product)

        if form.is_valid():
            form.save()
            return redirect(reverse('product_detail', args=[product_id]))
    context = {
        'form': form,
    }
    return render(request, 'store/edit_product.html', context)


@login_required
@user_passes_test(is_store_manager)
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    Product.objects.get(id=product_id).delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('store_view'))
