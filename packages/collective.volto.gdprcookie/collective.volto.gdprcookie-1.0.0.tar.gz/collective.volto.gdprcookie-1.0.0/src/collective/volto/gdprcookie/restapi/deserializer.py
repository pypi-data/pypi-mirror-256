from collective.volto.gdprcookie.interfaces import IGDPRCookieSettings
from plone.restapi.deserializer import json_body
from plone.restapi.deserializer.controlpanels import ControlpanelDeserializeFromJson
from plone.restapi.interfaces import IDeserializeFromJson
from zExceptions import BadRequest
from zope.component import adapter
from zope.interface import implementer

import json


@implementer(IDeserializeFromJson)
@adapter(IGDPRCookieSettings)
class GDPRCookieSettingsDeserializeFromJson(ControlpanelDeserializeFromJson):
    def __call__(self):
        """
        Convert json data into a string
        """
        req = json_body(self.controlpanel.request)
        proxy = self.registry.forInterface(self.schema, prefix=self.schema_prefix)
        errors = []

        gdpr_cookie_settings = req.get("gdpr_cookie_settings", {})
        if not gdpr_cookie_settings:
            errors.append(
                {
                    "message": "Missing data",
                    "field": "gdpr_cookie_settings",
                }
            )
            raise BadRequest(errors)
        try:
            setattr(proxy, "gdpr_cookie_settings", json.dumps(gdpr_cookie_settings))
        except ValueError as e:
            errors.append(
                {
                    "message": str(e),
                    "field": "gdpr_cookie_settings",
                    "error": e,
                }
            )

        if errors:
            raise BadRequest(errors)
