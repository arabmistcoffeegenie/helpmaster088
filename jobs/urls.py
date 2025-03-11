from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_cv, name='upload_cv'),
    path('results/', views.job_application_results, name='job_application_results'),
    path('list/', views.job_list, name='job_list'),
]
