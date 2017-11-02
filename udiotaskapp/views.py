from django.views.generic import ListView, CreateView, TemplateView
from django.shortcuts import reverse
from rest_framework import generics
from .models import Person
from .forms import PersonCreateForm, PersonFilterForm
from .serializers import PersonSerializer
# Create your views here.


class PersonCreateView(CreateView):
    """ View with PersonCreateForm for adding Person instances """
    model = Person
    form_class = PersonCreateForm

    def get_success_url(self):
        """ Redirects to list view """
        return reverse("person_list")


class PersonListView(ListView):
    """ PersonListView paginated_by 5 uses PersonFilterForm to filter query_set """
    model = Person
    form_class = PersonFilterForm
    paginate_by = 5
    context_object_name = "people"

    def get_context_data(self, **kwargs):
        """ Adds PersonFilterForm to context as 'form' """
        context = super(PersonListView, self).get_context_data(**kwargs)
        context['form'] = self.form_class
        return context

    def get_queryset(self):
        """ applies filters to queryset for GET['name'] && GET['email'] """
        filter_name = self.request.GET.get('name', '')  # blank '' as default = all
        filter_email = self.request.GET.get('email', '')  # blank '' as default = all
        return Person.objects.filter(name__icontains=filter_name, email__icontains=filter_email).order_by("name")


class PersonAPITemplateView(TemplateView):
    """ PersonAPITemplateView renders html that uses jQuery as a REST Client """
    template_name = "udiotaskapp/person_api.html"
    form_class = PersonFilterForm

    def get_context_data(self, **kwargs):
        """ Adds PersonFilterForm to context as 'form' """
        context = super(PersonAPITemplateView, self).get_context_data(**kwargs)
        context['form'] = self.form_class
        return context


class PersonAPIListView(generics.ListAPIView):
    """ PersonAPIListView extends ListAPIView that implements .list(request, args, **kwargs) """
    serializer_class = PersonSerializer
    model = Person

    def get_queryset(self):
        """ applies filters to queryset for GET['name'] && GET['email'] """
        filter_name = self.request.GET.get('name', '')
        filter_email = self.request.GET.get('email', '')
        return Person.objects.filter(name__icontains=filter_name, email__icontains=filter_email).order_by("name")
