from django.urls import path

from base_info import views

urlpatterns = [
    path('person-add-update.html', views.PersonAdd.as_view(), name='person_add'),
]
app_name = 'base_info'
