from django.shortcuts import render

def privacy_policy(request):
    return render(request, 'pages/privacy_policy.html')

def terms_conditions(request):
    return render(request, 'pages/terms_conditions.html')

def cancellation_refund(request):
    return render(request, 'pages/cancellation_refund.html')

def shipping_delivery(request):
    return render(request, 'pages/shipping_delivery.html')

def contact_us(request):
    return render(request, 'pages/contact_us.html')
