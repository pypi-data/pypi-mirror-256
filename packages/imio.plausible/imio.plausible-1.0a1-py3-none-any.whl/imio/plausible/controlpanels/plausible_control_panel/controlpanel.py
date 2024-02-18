# -*- coding: utf-8 -*-
from imio.plausible import _
from imio.plausible.interfaces import IImioPlausibleLayer
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.restapi.controlpanels import RegistryConfigletPanel
from plone.z3cform import layout
from zope import schema
from zope.component import adapter
from zope.interface import Interface


class IPlausibleControlPanel(Interface):
    url = schema.TextLine(
        title=_("Plausible URL"),
        description=_("Example : plausible.imio.be"),
        default="",
        required=False,
        readonly=False,
    )

    site = schema.TextLine(
        title=_("Plausible Site"),
        description=_("Example : imio.be"),
        default="",
        required=False,
        readonly=False,
    )

    token = schema.TextLine(
        title=_("Plausible token"),
        description=_("Plausible authentification token"),
        default="",
        required=False,
        readonly=False,
    )


class PlausibleControlPanel(RegistryEditForm):
    schema = IPlausibleControlPanel
    schema_prefix = "imio.plausible"
    label = _("Plausible Control Panel")


PlausibleControlPanelView = layout.wrap_form(
    PlausibleControlPanel, ControlPanelFormWrapper
)


@adapter(Interface, IImioPlausibleLayer)
class PlausibleControlPanelConfigletPanel(RegistryConfigletPanel):
    """Control Panel endpoint"""

    schema = IPlausibleControlPanel
    configlet_id = "plausible_control_panel-controlpanel"
    configlet_category_id = "Products"
    title = _("Plausible Control Panel")
    group = ""
    schema_prefix = "imio.plausible.plausible_control_panel"
