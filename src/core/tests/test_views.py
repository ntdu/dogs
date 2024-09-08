import json

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status

from src.core.models import Bread, Image
from src.core.tests.common import BreadTestCase


class BreadViewsetTestCase(BreadTestCase):
    def test_list_breads(self):
        url = reverse("breads-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(self.bread_names))

    def test_retrieve_bread(self):
        bread = Bread.objects.first()
        url = reverse("breads-detail", kwargs={"pk": bread.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], bread.name)

    def test_create_bread(self):
        url = reverse("breads-list")
        data = {
            "weight": json.dumps({"imperial": "10 - 20", "metric": "5 - 10"}),
            "height": json.dumps({"imperial": "9 - 11.5", "metric": "23"}),
            "external_id": 4,
            "name": "Bread4",
            "bred_for": "Small rodent hunting, lapdog",
            "breed_group": "Toy",
            "life_span": "10 - 12 years",
            "temperament": "Stubborn, Curious, Playful, Adventurous, Active, Fun-loving",
            "reference_image_id": "123",
        }
        response = self.client.post(url, data, format="json")
        code, count, data = self.parse_response(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(code, status.HTTP_201_CREATED)

        self.assertEqual(Bread.objects.count(), len(self.bread_names) + 1)
        self.assertEqual(Bread.objects.get(name="Bread4").name, "Bread4")


class ImageViewsetTestCase(BreadTestCase):
    def setUp(self):
        super().setUp()
        self.bread = Bread.objects.first()
        self.image_names = ["Image1", "Image2", "Image3"]
        for name in self.image_names:
            Image.objects.create(file="path/to/file", type="image/jpeg", name=name, size=5000, bread=self.bread)

    def test_list_images(self):
        url = reverse("images-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(self.image_names))

    def test_retrieve_image(self):
        image = Image.objects.first()
        url = reverse("images-detail", kwargs={"pk": image.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], image.name)

    def test_create_image(self):
        url = reverse("images-list")
        file = SimpleUploadedFile("file.jpg", b"file_content", content_type="image/jpeg")
        data = {"file": file, "type": "image/jpeg", "bread": self.bread.id}
        response = self.client.post(url, data)
        code, count, data = self.parse_response(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(code, status.HTTP_201_CREATED)
        self.assertEqual(Image.objects.count(), len(self.image_names) + 1)

    # def test_display_image(self):
    #     image = Image.objects.first()
    #     url = reverse('images-display', kwargs={'pk': image.id})
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     # self.assertIsInstance(response, FileResponse)
    #     # self.assertEqual(response.file.name, image.file.name)

    def test_random_images(self):
        url = reverse("images-random_images")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), min(20, Image.objects.count()))
        for image_data in data:
            self.assertIn("name", image_data)
            self.assertIn(image_data["name"], self.image_names)
