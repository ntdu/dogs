from django.test import TestCase

from src.core.models import Bread


class BreadTestCase(TestCase):
    def setUp(self):
        self.bread_names = ["Bread1", "Bread2", "Bread3"]
        for name in self.bread_names:
            Bread.objects.create(
                weight={"imperial": "10 - 20", "metric": "5 - 10"},
                height={"imperial": "9 - 11.5", "metric": "23"},
                external_id=1,
                name=name,
                bred_for="Small rodent hunting, lapdog",
                breed_group="Toy",
                life_span="10 - 12 years",
                temperament="Stubborn, Curious, Playful, Adventurous, Active, Fun-loving",
            )

    def parse_response(self, response):
        return response.json().get("code"), response.json().get("count"), response.json().get("data")
