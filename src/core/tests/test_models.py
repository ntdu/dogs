from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from src.core.models import Bread, Image


class ModelTests(TestCase):
    """Test models."""

    def test_create_bread(self):
        """Test creating a bread is successful."""

        recipe = Bread.objects.create(
            weight={"imperial": "10 - 20", "metric": "5 - 10"},
            height={"imperial": "9 - 11.5", "metric": "23"},
            external_id=1,
            name="Affenpinscher",
            bred_for="Small rodent hunting, lapdog",
            breed_group="Toy",
            life_span="10 - 12 years",
            temperament="Stubborn, Curious, Playful, Adventurous, Active, Fun-loving",
        )

        self.assertEqual(recipe.external_id, 1)

    def test_bread_str(self):
        """Test the bread string representation."""
        bread = Bread.objects.create(
            weight={"imperial": "10 - 20", "metric": "5 - 10"},
            height={"imperial": "9 - 11.5", "metric": "23"},
            external_id=1,
            name="Affenpinscher",
            bred_for="Small rodent hunting, lapdog",
            breed_group="Toy",
            life_span="10 - 12 years",
            temperament="Stubborn, Curious, Playful, Adventurous, Active, Fun-loving",
        )
        self.assertEqual(str(bread), f"{bread.external_id} | {bread.name}")


class TestImageModel(TestCase):
    """Test Image model."""

    def setUp(self):
        self.bread = Bread.objects.create(
            weight={"imperial": "10 - 20", "metric": "5 - 10"},
            height={"imperial": "9 - 11.5", "metric": "23"},
            external_id=1,
            name="Affenpinscher",
            bred_for="Small rodent hunting, lapdog",
            breed_group="Toy",
            life_span="10 - 12 years",
            temperament="Stubborn, Curious, Playful, Adventurous, Active, Fun-loving",
        )

    def test_create_image(self):
        """Test creating an image is successful."""

        image_file = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        image = Image.objects.create(
            bread=self.bread,
            name="Test Image",
            file=image_file,
            type="jpg",
            size=100,
        )

        self.assertEqual(image.bread, self.bread)
        self.assertEqual(image.name, "Test Image")
        self.assertEqual(image.type, "jpg")
        self.assertEqual(image.size, 100)

    def test_image_str(self):
        """Test the image string representation."""
        image_file = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        image = Image.objects.create(
            bread=self.bread,
            name="Test Image",
            file=image_file,
            type="jpg",
            size=100,
        )
        self.assertEqual(str(image), f"{image.id} | {image.name}")
