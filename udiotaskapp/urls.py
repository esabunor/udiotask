from django.conf.urls import url
from .views import PersonCreateView, PersonListView, PersonAPIListView, PersonAPITemplateView


urlpatterns = [
    url(r'^people/$', PersonListView.as_view(), name="person_list"),
    url(r'^add-person/$', PersonCreateView.as_view(), name="person_create"),
    url(r'^api/people/$', PersonAPIListView.as_view(), name="person_api_list"),
    url(r'^api/people/search/$', PersonAPITemplateView.as_view(), name="person_api_search"),
]
