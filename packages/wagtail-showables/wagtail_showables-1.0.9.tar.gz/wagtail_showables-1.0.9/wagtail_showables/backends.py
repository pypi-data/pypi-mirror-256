from abc import ABC, abstractmethod
from django.db import transaction
from django.utils.module_loading import import_string
from django.core.cache import (
    caches,
    DEFAULT_CACHE_ALIAS,
)
from .models import ShowableRegistry
from .options import (
    SHOWABLES_BACKEND,
    SHOWABLES_DEFAULT_BACKEND,
)


def get_showable_backend(showables_backend: str = SHOWABLES_DEFAULT_BACKEND) -> "ShowableBackend":
    try:
        backend_dict = SHOWABLES_BACKEND[showables_backend]
    except KeyError as e:
        raise KeyError(f"Invalid showables backend configuration: {e}") from e
    
    try:
        backend_class = backend_dict["CLASS"]
        backend_options = backend_dict["OPTIONS"]
        backend = import_string(backend_class)
    except ImportError as e:
        raise ImportError(f"Could not import the showables backend: {e}") from e
        
    except KeyError as e:
        raise KeyError(f"Invalid showables backend configuration: {e}") from e
    
    return backend(**backend_options)


class ShowableBackend(ABC):

    @abstractmethod
    def process_registry(self, data: dict):
        pass

    @abstractmethod
    def registry_data(self) -> dict:
        pass

    @abstractmethod
    def is_shown(self, block):
        pass

    def renew(self):
        """
            Renew the backend's data in case of long-living objects.
            Might be useful for model-based backends.
            This is not to be used for garbage collection.
        """
        pass



class ShowableCacheBackend(ShowableBackend):
    def __init__(self, cache_key: str = "wagtail_showables", cache_backend: str = DEFAULT_CACHE_ALIAS):
        self.cache_backend = cache_backend
        self.cache = caches[cache_backend]
        self.cache_key = cache_key
        self._data = {}

    def process_registry(self, data: dict):
        self.cache.set(self.cache_key, data)
        if hasattr(self.cache, "persist"):
            self.cache.persist(self.cache_key)
        self._data = data

    def registry_data(self) -> dict:
        self._data = self.cache.get(self.cache_key, {})
        return self._data

    def is_shown(self, data_key: str) -> bool:
        data = self._data or self.registry_data() or {}
        return data.get(data_key, None) not in [False, None]
        
    def renew(self):
        self._data = self.cache.get(self.cache_key, {})
        return self._data
    
import threading

_performance_backend_data = threading.local()


class ShowablePerformanceCacheBackend(ShowableCacheBackend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self._data # We don't need this anymore

    def process_registry(self, data: dict):
        self.cache.set(self.cache_key, data)
        if hasattr(self.cache, "persist"):
            self.cache.persist(self.cache_key)
        _performance_backend_data.data = data

    def registry_data(self) -> dict:
        data = getattr(_performance_backend_data, "data", None)
        if data is None:
            raise ValueError("The data has not been set, are you using the ShowablePerformanceDataMiddleware?")
        return data
    
    def fetch_registry_data(self):
        return self.cache.get(self.cache_key, {}) or {}
    
    def is_shown(self, data_key: str) -> bool:
        data = self.registry_data()
        return data.get(data_key, None) not in [False, None]
    
    def renew(self):
        """
            Renew is not used for this backend.
            _performance_backend_data is a thread-local object.
            It only lives for the duration of the request.
        """
        pass


class ShowablePerformanceDBBackend(ShowableBackend):

    @transaction.atomic
    def process_registry(self, data: dict):
        registry = ShowableRegistry.load()
        registry.data = data
        registry.save()

    def registry_data(self) -> dict:
        data = getattr(_performance_backend_data, "data", None)
        if data is None:
            raise ValueError("The data has not been set, are you using the ShowablePerformanceDataMiddleware?")
        return data
    
    def is_shown(self, data_key: str) -> bool:
        data = self.registry_data()
        return data.get(data_key, None) not in [False, None]
    
    def fetch_registry_data(self):
        registry = ShowableRegistry.load()
        return registry.data or {}
    
    def renew(self):
        """
            Renew is not used for this backend.
            _performance_backend_data is a thread-local object.
            It only lives for the duration of the request.
        """
        pass

