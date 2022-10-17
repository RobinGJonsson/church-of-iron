from django.shortcuts import render


def checkout_view(request):

    context = {

    }

    return render(request, 'checkout/checkout.html', context)
