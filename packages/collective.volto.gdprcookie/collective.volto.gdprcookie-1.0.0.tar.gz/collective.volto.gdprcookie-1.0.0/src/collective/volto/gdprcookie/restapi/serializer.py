from collective.volto.gdprcookie.interfaces import IGDPRCookieSettings
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer.controlpanels import ControlpanelSerializeToJson
from zope.component import adapter
from zope.interface import implementer

import json
import logging


logger = logging.getLogger(__name__)


@implementer(ISerializeToJson)
@adapter(IGDPRCookieSettings)
class GDPRCookieSettingsSerializeToJson(ControlpanelSerializeToJson):
    def __call__(self):
        json_data = super().__call__()
        gdpr_cookie_settings = json_data["data"].get("gdpr_cookie_settings", "{}")
        try:
            json_data["data"]["gdpr_cookie_settings"] = json.loads(gdpr_cookie_settings)
        except json.decoder.JSONDecodeError:
            logger.error(
                f"Unable to convert value into json object: {gdpr_cookie_settings}"
            )
        return json_data
