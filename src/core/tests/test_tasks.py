from unittest.mock import MagicMock, patch

from django.test import TestCase

from src.api.dogs.tasks import sync_breads


@patch("src.api.dogs.tasks.send_external_api_request")
@patch("src.api.dogs.tasks.Bread.objects.last")
@patch("src.api.dogs.tasks.Bread.objects.bulk_create")
class TestSyncBreads(TestCase):
    def test_sync_breads(self, mock_bulk_create, mock_last, mock_request):
        # Mock the response from the external API
        mock_request.return_value.json.return_value = [
            {
                "weight": {"imperial": "10 - 20", "metric": "5 - 10"},
                "height": {"imperial": "9 - 11.5", "metric": "23"},
                "id": 1,
                "name": "Affenpinscher",
                "bred_for": "Small rodent hunting, lapdog",
                "breed_group": "Toy",
                "life_span": "10 - 12 years",
                "temperament": "Stubborn, Curious, Playful, Adventurous, Active, Fun-loving",
                "reference_image_id": "123",
            }
        ]

        # Mock the last bread in the database
        mock_last.return_value = None

        # Call the function
        result = sync_breads()

        # Check that the function returned "Success"
        self.assertEqual(result, "Success")

        # Check that bulk_create was called with the correct arguments
        mock_bulk_create.assert_called_once()

    def test_sync_breads_invalid_input(self, mock_bulk_create, mock_last, mock_request):
        # Mock the response from the external API
        mock_request.return_value.json.return_value = [{"id": 1, "name": "Test Bread", "origin": "Test Origin"}]

        # Mock the last bread in the database
        mock_last.return_value = None

        # Call the function
        result = sync_breads()

        # Check that the function returned "Success"
        self.assertEqual(result, "No new breads to sync")

        # Check that bulk_create was not called
        mock_bulk_create.assert_not_called()

    def test_sync_breads_no_new_breads(self, mock_bulk_create, mock_last, mock_request):
        # Mock the response from the external API
        mock_request.return_value.json.return_value = [
            {
                "id": 1,
                "name": "Affenpinscher",
                "bred_for": "Small rodent hunting, lapdog",
                "breed_group": "Toy",
                "life_span": "10 - 12 years",
                "temperament": "Stubborn, Curious, Playful, Adventurous, Active, Fun-loving",
            }
        ]

        # Mock the last bread in the database
        mock_last.return_value = MagicMock(external_id=1)

        # Call the function
        result = sync_breads()

        # Check that the function returned "No new breads to sync"
        self.assertEqual(result, "No new breads to sync")

        # Check that bulk_create was not called
        mock_bulk_create.assert_not_called()
