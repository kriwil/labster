from labster.forms import ErrorInfoForm
from labster.views import BaseLabProxyLogView


class LogError(BaseLabProxyLogView):
    form_class = ErrorInfoForm


log_error = LogError.as_view()
