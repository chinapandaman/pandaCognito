# -*- coding: utf-8 -*-


from jsonschema import ValidationError, validate

from cognito import Cognito
from gluon import HTTP


@auth.allows_jwt()
@auth.requires_login()
@request.restful()
def create_group():
    schema = {
        "type": "object",
        "properties": {
            "GroupName": {"type": "string"},
            "Description": {"type": "string"},
        },
        "required": ["GroupName", "Description"],
    }

    def POST(*reqargs, **reqvars):
        try:
            validate(instance=reqvars, schema=schema)
        except ValidationError:
            raise HTTP(400, "InvalidParameterException")

        group_name = reqvars["GroupName"]
        description = reqvars["Description"]

        return response.json(Cognito().create_group(group_name, description))

    return locals()


@auth.allows_jwt()
@auth.requires_login()
@request.restful()
def sign_up():
    schema = {
        "type": "object",
        "properties": {
            "Username": {"type": "string"},
            "Password": {"type": "string"},
            "UserAttributes": {"type": "object"},
        },
        "required": ["Username", "Password"],
    }

    def POST(*reqargs, **reqvars):
        try:
            validate(instance=reqvars, schema=schema)
        except ValidationError:
            raise HTTP(400, "InvalidParameterException")

        username = reqvars["Username"]
        password = reqvars["Password"]
        user_attributes = reqvars.get("UserAttributes")

        return response.json(Cognito().sign_up(username, password, user_attributes))

    return locals()
