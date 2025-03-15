from django.urls import path
from . import views

urlpatterns = [
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms/', views.terms_conditions, name='terms_conditions'),
    path('cancellation-refund/', views.cancellation_refund, name='cancellation_refund'),
    path('shipping-delivery/', views.shipping_delivery, name='shipping_delivery'),
    path('contact-us/', views.contact_us, name='contact_us'),
]
