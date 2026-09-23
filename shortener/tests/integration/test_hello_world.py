from django.test import SimpleTestCase
from django.urls import reverse


class HelloWorldTests(SimpleTestCase):
    def test_get_returns_hello_world_json(self) -> None:
        response = self.client.get(reverse('hello-world'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.json(), {'message': 'Hello world'})
