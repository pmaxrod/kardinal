from django.utils.translation import gettext as _
from wagtail import hooks
from wagtail.admin.views.account import BaseSettingsPanel, SettingsTab
from users.forms import UserProfileSettingsForm

custom_tab = SettingsTab(name="app", title="App", order=150)


@hooks.register("register_account_settings_panel")
class UserProfileSettingsPanel(BaseSettingsPanel):
    name = "custom"
    title = _("Biografía del usuario")
    order = 100
    form_class = UserProfileSettingsForm
    tab = custom_tab
    form_object = "user"
    template_name = "users/admin/custom_settings.html"
