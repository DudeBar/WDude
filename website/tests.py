from django.test import TestCase

# Create your tests here.
from website.models import Customer


class CustomerTestCase(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create(login="test_user", password="test_user")

    def test_customer_create(self):
        response = self.client.post("/customer_create",
                                    {
                                        'login': "test",
                                        'password': "test",
                                        'confirm_password': "test"
                                    })
        self.assertEquals(response.status_code, 302)
        self.assertTrue(Customer.objects.filter(login="test").exists())

    def test_customer_login(self):
        response = self.client.post("/login",
            {
                'login': "test_user",
                'password':"test_user"
            })
        self.assertEquals(response.status_code, 302)

    def test_customer_login_wrong_password(self):
        response = self.client.post("/login",
            {
                'login': "test_user",
                'password':"wrong_pass"
            })
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Le mot de passe n&#39;est pas correct")

    def test_customer_login_wrong_login(self):
        response = self.client.post("/login",
            {
                'login': "wrong_user",
                'password':"wrong_pass"
            })
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Le login n&#39;es pas correct")