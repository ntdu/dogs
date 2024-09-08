from src.api.dogs.filters import BreadFilter
from src.core.models import Bread
from src.core.tests.common import BreadTestCase


class TestBreadFilter(BreadTestCase):
    def test_filter_name(self):
        # Apply the filter
        f = BreadFilter({"name": "Bread1,Bread2"}, queryset=Bread.objects.all())

        # Check that the filter correctly filters the queryset
        self.assertEqual(f.qs.count(), 2)
        self.assertEqual(set(bread.name for bread in f.qs), {"Bread1", "Bread2"})
