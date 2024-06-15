import json
from uuid import UUID

from rest_framework.exceptions import ValidationError
from rest_framework.renderers import BaseRenderer

from apps.core.response import DevidResponse, DevidStatus, errors_messages

class CustomJSONRenderer(BaseRenderer):
    media_type = "application/json"
    format = "json"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context.get("response").status_code in (200, 201, 204):
            response_data = DevidResponse.get_response(
                success=True,
                message="Success",
                status=DevidStatus.Success.value,
                response=data,
            )
        else:
            response_data = DevidResponse.get_response(
                success=False,
                message="Something went wrong.",
                status=DevidStatus.Error.value,
                error=errors_messages(ValidationError(data)),
            )
        return json.dumps(response_data, cls=UUIDEncoder)



class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        return super().default(obj)