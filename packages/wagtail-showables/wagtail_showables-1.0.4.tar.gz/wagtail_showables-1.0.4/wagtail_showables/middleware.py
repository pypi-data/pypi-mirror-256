import warnings
from .backends import (
    get_showable_backend,
    _performance_backend_data,
    ShowablePerformanceCacheBackend,
    ShowablePerformanceDBBackend,
)

class ShowablePerformanceDataMiddleware:
    """Middleware that saves request in thread local storage."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        backend = get_showable_backend()

        if not isinstance(backend, (ShowablePerformanceCacheBackend, ShowablePerformanceDBBackend)):
            warnings.warn(
                "You are using the ShowablePerformanceDataMiddleware without the ShowablePerformanceCacheBackend. "
                "This middleware will have no effect."
            )
            return self.get_response(request)

        _performance_backend_data.data = backend.fetch_registry_data()
        response = self.get_response(request)
        del _performance_backend_data.data
        return response
