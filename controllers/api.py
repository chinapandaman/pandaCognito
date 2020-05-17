# -*- coding: utf-8 -*-


from cognito import Cognito


@request.restful()
def sign_up():
    def POST(*reqargs, **reqvars):
        username = reqvars["Username"]
        password = reqvars["Password"]
        user_attributes = reqvars.get("UserAttributes")

        return response.json(Cognito().sign_up(username, password, user_attributes))

    return locals()
