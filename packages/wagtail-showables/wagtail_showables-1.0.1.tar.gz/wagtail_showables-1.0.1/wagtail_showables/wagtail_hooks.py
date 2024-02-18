from wagtail import hooks
from django.urls import path
from django.utils.html import format_html
from django.templatetags.static import static

from .views import (
    showables_list,
    showables_edit,
)


@hooks.register("insert_global_admin_css")
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static("wagtail_showables/css/showables.css"),
    )


# wagtail_showables_showables_list
# wagtail_showables_enable_disable_blocks

@hooks.register("register_admin_urls")
def register_admin_urls():
    return [
        path("showables/", showables_list, name="wagtail_showables_showables_list"),
        path("showables/edit/", showables_edit, name="wagtail_showables_enable_disable_blocks"),
    ]

