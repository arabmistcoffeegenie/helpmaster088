from django.urls import path
from . import views

urlpatterns = [
    path('upgrade/', views.upgrade_view, name='upgrade'),
    path('success/', views.payment_success_view, name='payment_success'),
    path('cancel/', views.payment_cancel_view, name='payment_cancel'),
]
