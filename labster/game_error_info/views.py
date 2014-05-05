from rest_framework.permissions import IsAuthenticated

from labster.authentication import SingleTokenAuthentication
from labster.forms import ErrorInfoForm
from labster.views import BaseLabProxyLogView


class LogError(BaseLabProxyLogView):

    authentication_classes = (SingleTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    form_class = ErrorInfoForm


log_error = LogError.as_view()
