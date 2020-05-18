# -*- coding: utf-8 -*-


from jsonschema import ValidationError, validate

from cognito import Cognito
from gluon import HTTP


@auth.allows_jwt()
@auth.requires_login()
@request.restful()
def sign_up():
    def POST(*reqargs, **reqvars):
        schema = {
            "type": "object",
            "properties": {
                "Username": {"type": "string"},
                "Password": {"type": "string"},
                "UserAttributes": {"type": "object"},
            },
            "required": ["Username", "Password"],
        }

        try:
            validate(instance=reqvars, schema=schema)
        except ValidationError:
            raise HTTP(404, "InvalidParameterException")

        username = reqvars["Username"]
        password = reqvars["Password"]
        user_attributes = reqvars.get("UserAttributes")

        return response.json(Cognito().sign_up(username, password, user_attributes))

    return locals()
