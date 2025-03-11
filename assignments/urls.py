from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_assignment, name='submit_assignment'),
    path('list/', views.assignment_list, name='assignment_list'),
    path('pay-per-assignment/', views.pay_per_assignment, name='pay_per_assignment'),
    path('pay-per-assignment/success/', views.pay_per_assignment_success, name='pay_per_assignment_success'),
]
