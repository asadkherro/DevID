from enum import Enum

from .typings import TypedResponse

class DevidResponse:
    @staticmethod
    def get_response(
        success: str = False,
        message: str = "",
        status: int = 101,
        error_code: int = 400,
        response: dict = {},
        error: dict = {},
    ) -> TypedResponse:
        return {
            "success": success,
            "status": status,
            "message": message,
            "response": response,
            "error": error,
        }


class DevidStatus(Enum):
    Success = 1
    Error = 101


def errors_messages(errors):
    errors = errors.get_full_details()
    error_dict = {}
    try:
        for field, error_list in errors.items():
            try:
                error_dict[field] = {
                    "error_string": error_list[0].get("message").replace('"', ""),
                    "error_code": error_list[0].get("code"),
                }
            except KeyError:
                error_dict[field] = {
                    "error_string": error_list.get("message").replace('"', ""),
                    "error_code": error_list.get("code"),
                }
    except:
        try:
            error_dict["non_fields"] = {
                "error_string": errors[0].get("message").replace('"', ""),
                "error_code": errors[0].get("code"),
            }
        except:
            error_dict["non_fields"] = {
                "error_string": errors.get("detail").get("message").replace('"', ""),
                "error_code": errors.get("detail").get("code"),
            }
    return error_dict
