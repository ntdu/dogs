import logging

from django.db import transaction

from src.api.dogs.serializers import BreadSerializer
from src.core.models import Bread
from src.media_service.celery_settings import app
from src.media_service.service_settings import get_settings
from src.utils.http import send_external_api_request

service_settings = get_settings()
logger = logging.getLogger(__name__)


@app.task(queue="tasks")
def sync_breads():
    # Send a request to the external API
    response = send_external_api_request(
        method="GET",
        url=f"{service_settings.breads_url}",
        headers={"Content-Type": "application/json", "x-api-key": service_settings.DOGS_API_KEY},
    )

    lastest_bread = Bread.objects.last()
    response = response.json()
    # Filter out the breads that are already in the database
    if lastest_bread:
        lastest_bread_id = lastest_bread.external_id
        response.sort(key=lambda x: x["id"])

        response = [bread for bread in response if bread["id"] > lastest_bread_id]

    bread_instances = []
    for bread in response:
        bread["external_id"] = bread.pop("id")
        serializer = BreadSerializer(data=bread)
        if serializer.is_valid():
            bread_instance = Bread(**serializer.validated_data)
            bread_instances.append(bread_instance)
        else:
            print(f"Error while serializing bread: {bread=} | {serializer.errors=}")
            logger.error(f"Error while serializing bread: {bread=} | {serializer.errors=}")

    if not bread_instances:
        return "No new breads to sync"

    with transaction.atomic():
        Bread.objects.bulk_create(bread_instances)

    return "Success"
