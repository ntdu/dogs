from src.api.dogs.serializers import BreadSerializer
from src.media_service.celery_settings import app
from src.media_service.service_settings import get_settings
from src.utils.http import send_external_api_request

service_settings = get_settings()


@app.task(queue="tasks")
def sync_breads():
    # Send a request to the external API
    response = send_external_api_request(
        method="GET",
        url=f"{service_settings.breads_url}?limit=2",
        headers={
            # 'Content-Type': 'application/json',
            "x-api-key": service_settings.DOGS_API_KEY
        },
    )
    print(response.json())
    for bread in response.json():
        bread["external_id"] = bread.pop("id")
        serializer = BreadSerializer(data=bread)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
    # print(response.json())
    return "Success"
