import json
from django.test import TestCase
from django.shortcuts import reverse
from rest_framework.test import APITestCase
from .models import Person
from .forms import PersonFilterForm
# Create your tests here.


class PersonCreateViewTest(TestCase):
    """ TestCase for PersonCreateView """
    def test_person_creation(self):
        """ test url redirection after successful user creation """
        data = {"name": "john", "email": "john@doe.com"}
        response = self.client.post(reverse('person_create'), data, follow=True)
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.redirect_chain[0][0], reverse("person_list"))

    def test_person_creation_with_existing_email(self):
        """ test form error handling when populated with an existing email"""
        data = {"name": "john", "email": "john@doe.com"}
        self.client.post(reverse('person_create'), data, follow=True)
        response = self.client.post(reverse('person_create'), data, follow=True)
        self.assertTrue("form" in response.context)
        self.assertIsNotNone(response.context['form'].errors)
        form = response.context['form']
        self.assertEqual(form.email.errors, "email already exists")


class PersonAPIListViewTest(APITestCase):
    """ TestCase for PersonAPIListView extends rest_framework.test.APITestCase """
    @classmethod
    def setUpTestData(cls):
        """ Create Person instances """
        Person.objects.bulk_create([
            Person(name="john", email="john@foo.com"),
            Person(name="doe", email="doe@foo.com"),
        ])
        super(PersonAPIListViewTest, cls).setUpTestData()

    def test_api_list_display(self):
        """ tests views response """
        response = self.client.get(reverse("person_api_list"))
        data = [
            {"name": "john", "email": "john@foo.com"},
            {"name": "doe", "email": "doe@foo.com"}
        ]
        self.assertEqual(json.loads(response.content), data)


class PersonListView(TestCase):
    """ TestCase for PersonListView """
    @classmethod
    def setUpTestData(cls):
        Person.objects.bulk_create([
            Person(name="john", email="john@foo.com"),
            Person(name="doe", email="doe@foo.com"),
            Person(name="bar", email="bar@foo.com"),
            Person(name="chris", email="chris@foo.com"),
            Person(name="david", email="david@foo.com"),
            Person(name="mike", email="mike@foo.com"),
        ])
        super(PersonListView, cls).setUpTestData()

    def test_pagination(self):
        """ test listviews pagination """
        response = self.client.get(reverse('person_list'))
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])

    def test_search_result(self):
        """ test person list filtering """
        data = {"name": "john", "email": "foo"}
        response = self.client.get(reverse("person_list"), data)
        context = response.context
        self.assertTrue("people" in context)
        self.assertEqual(len(context['people']), 1)


class PersonFilterFormTest(TestCase):
    """ PersonFilterForm TestCase """
    def test_filter_form_valid_data(self):
        """ test PersonFilterForm with valid data """
        form = PersonFilterForm(data={"name": "john", "email": "john@foo.com"})
        self.assertTrue(form.is_valid())
