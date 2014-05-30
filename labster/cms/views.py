from edxmako.shortcuts import render_to_response


def lab_list(self):
    template_name = "labster/lab_list.html"
    context = {
    }
    return render_to_response(template_name, context)
