from labster.forms import DeviceInfoForm
from labster.views import BaseLabProxyLogView


class LogDevice(BaseLabProxyLogView):
    form_Class = DeviceInfoForm


log_device = LogDevice.as_view()
