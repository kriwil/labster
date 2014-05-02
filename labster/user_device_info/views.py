from labster.forms import DeviceInfoForm
from labster.views import BaseLabProxyLogView


class LogDevice(BaseLabProxyLogView):
    form_class = DeviceInfoForm


log_device = LogDevice.as_view()
