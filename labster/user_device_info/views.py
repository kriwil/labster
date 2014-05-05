from rest_framework.permissions import IsAuthenticated

from labster.authentication import SingleTokenAuthentication
from labster.forms import DeviceInfoForm
from labster.views import BaseLabProxyLogView


class LogDevice(BaseLabProxyLogView):
    authentication_classes = (SingleTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    form_class = DeviceInfoForm


log_device = LogDevice.as_view()
