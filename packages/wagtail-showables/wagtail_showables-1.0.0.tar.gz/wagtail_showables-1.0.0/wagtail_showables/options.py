from functools import cache
from django.conf import settings
from django.utils.translation import gettext_lazy as _

LEVEL_NONE = 0
LEVEL_SHOW = 1
LEVEL_EDIT = 2

ADMIN_INTERACTION_LEVEL = getattr(
    settings, "WAGTAIL_SHOWABLES_ADMIN_INTERACTION_ENABLED", LEVEL_NONE
)

DISABLED_DISPLAY_TEXT = getattr(
    settings, "WAGTAIL_SHOWABLES_DISABLED_DISPLAY_TEXT", _("This block is disabled.")
)

SHOWABLES_DEFAULT_BACKEND = getattr(
    settings, "WAGTAIL_SHOWABLES_DEFAULT_BACKEND", "default"
)

SHOWABLES_BACKEND = getattr(
    settings, "WAGTAIL_SHOWABLES_BACKEND", {
        "default": {
            "CLASS": "wagtail_showables.backends.ShowableCacheBackend",
            "OPTIONS": {
                "cache_key": "wagtail_showables_registry",
                "cache_backend": "default",
            },
        },
        "performance_cache": {
            "CLASS": "wagtail_showables.backends.ShowablePerformanceCacheBackend",
            "OPTIONS": {
                "cache_key": "wagtail_showables_registry",
                "cache_backend": "cache",
            },
        },
        "performance_db": {
            "CLASS": "wagtail_showables.backends.ShowablePerformanceDBBackend",
            "OPTIONS": {},
        },
    }
)
