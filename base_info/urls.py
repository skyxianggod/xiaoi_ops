from django.urls import path

from base_info import views

urlpatterns = [
    path('person.html', views.PersonList.as_view(), name='person_list'),
    path('person-add-update.html', views.PersonAdd.as_view(), name='person_add'),
    path('person-del.html', views.PersonDel.as_view(), name='person_del'),
    path('person-add-update-<pk>.html', views.PersonUpdate.as_view(), name='person_update'),
]
app_name = 'base_info'
