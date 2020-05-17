# -*- coding: utf-8 -*-


from gluon import DAL, Field, current
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth


class Cognito(object):
    def __init__(self):
        self.db = DAL(
            current.config.get("cognito_db.uri"),
            pool_size=current.config.get("cognito_db.pool_size"),
            migrate_enabled=current.config.get("cognito_db.migrate"),
            check_reserved=["all"],
        )

        self.auth = Auth(db=self.db, host_names=current.config.get("host.names"))

        # TODO: extend this during implementation
        self.auth.settings.extra_fields["auth_user"] = [
            Field("user_attributes", type="json")
        ]

        self.auth.define_tables(username=True, signature=False)

    def sign_up(self, username, password, user_attributes):
        result = self.auth.register_bare(username=username, password=password)

        result.update_record(user_attributes=user_attributes)

        return {
            "UserConfirmed": not self.auth.settings.registration_requires_verification,
            "UserSub": result.id,
        }
