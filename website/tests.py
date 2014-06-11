from django.test import TestCase

# Create your tests here.
from website.models import Customer


class CustomerTestCase(TestCase):

    def test_customer_create(self):
        response = self.client.post("/customer_create",
                                    {
                                    'login': "test",
                                    'password': "test",
                                    'confirm_password': "test"
                                    })
        self.assertEquals(response.status_code, 302)
        self.assertTrue(Customer.objects.filter(login="test").exists())

