# -*- coding: utf-8 -*-


from gluon import DAL, HTTP, Field, current
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

        self.auth.settings.create_user_groups = None

        # TODO: extend this during implementation
        self.auth.settings.extra_fields["auth_user"] = [
            Field("user_attributes", type="json")
        ]

        self.auth.define_tables(username=True, signature=True)

    def admin_add_user_to_group(self, username, group_name):
        user = self.db(self.db.auth_user.username == username).select()
        if not len(user):
            raise HTTP(400, "UserNotFoundException")

        group = self.db(self.db.auth_group.role == group_name).select()

        if len(group):
            self.auth.add_membership(group.first().id, user.first().id)

        return None

    def create_group(self, group_name, description):
        if len(self.db(self.db.auth_group.role == group_name).select()):
            raise HTTP(400, "GroupExistsException")

        result = self.auth.add_group(role=group_name, description=description)

        group = self.db(self.db.auth_group.id == result).select().first()

        return {
            "Group": {
                "GroupName": group["role"],
                "Description": group["description"],
                "LastModifiedDate": group["modified_on"],
                "CreationDate": group["created_on"],
            }
        }

    def delete_group(self, group_name):
        self.db(self.db.auth_group.role == group_name).delete()

        return None

    def sign_up(self, username, password, user_attributes):
        result = self.auth.register_bare(username=username, password=password)

        if not result:
            raise HTTP(400, "UsernameExistsException")

        result.update_record(user_attributes=user_attributes)

        return {
            "UserConfirmed": not self.auth.settings.registration_requires_verification,
            "UserSub": result.id,
        }
