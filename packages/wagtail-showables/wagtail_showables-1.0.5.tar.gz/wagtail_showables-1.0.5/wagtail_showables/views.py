from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from django.contrib import messages
from .backends import (
    get_showable_backend,
)
from .registry import (
    get_registry_form,
    get_sorted_registry,
    RegisteredBlock,
)



def showables_list(request: HttpRequest):
    if not request.user.has_perm("wagtail_showables.can_view_showables"):
        messages.error(request, _("You do not have the permissions to view or edit showables."))
        return redirect("wagtailadmin_home")

    registry = get_sorted_registry()

    return render(request, "wagtail_showables/showables_admin_list.html", {
        "registry": registry,
    })


def showables_edit(request: HttpRequest):
    registry = get_sorted_registry()
    form_class = get_registry_form()
    form = form_class(request.POST or None)

    if not request.user.has_perms([
        "wagtail_showables.can_toggle_showing",
        "wagtail_showables.can_view_showables",
    ]):
        messages.error(request, _("You do not have the permissions to view or edit showables."))
        return redirect("wagtailadmin_home")
    
    if request.method == "POST" and form.is_valid():
        data = form.to_dict()
        for block in registry:
            block.is_shown = data.get(block.import_path, False)

        backend = get_showable_backend()
        backend.process_registry(data)

        messages.success(request, _("Showables have been updated."))
        
        return redirect("wagtail_showables_showables_list")
    
    elif request.method == "POST":
        messages.error(request, _("Something has gone wrong with your form submission."))
    
    return render(request, "wagtail_showables/showables_admin_form.html", {
        "registry": registry,
        "form": form,
    })
