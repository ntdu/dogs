import logging
import traceback

from rest_framework import exceptions, status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import set_rollback

logger = logging.getLogger(__name__)


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context["response"].status_code
        renderer_context["response"].status_code = status.HTTP_200_OK
        response = {
            "code": status_code,
            # "count": len(data) if isinstance(data, list) else 0,
            # "data": data,
            "count": data.get("count", 0),
            "data": data.get("results", data),
        }
        return super().render(response, accepted_media_type, renderer_context)


def custom_exception_handler(exc, context):
    if isinstance(exc, exceptions.APIException):
        pass

    if isinstance(exc, Exception):

        tb = traceback.TracebackException.from_exception(exc)
        frame = tb.stack[-1]
        logger.exception(
            f"Exception: {exc.__class__.__name__} - {exc} in {frame.name} at line {frame.lineno} in {frame.filename}"
        )

        set_rollback()

        return Response({"error": exc.__class__.__name__}, status=500)

    return None
