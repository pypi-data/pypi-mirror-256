from html import escape
from django import forms
from wagtail import blocks
import copy

from .backends import (
    get_showable_backend,
)
from .options import (
    LEVEL_NONE as ADMIN_INTERACTION_LEVEL_NONE,
    LEVEL_SHOW as ADMIN_INTERACTION_LEVEL_SHOW,
    LEVEL_EDIT as ADMIN_INTERACTION_LEVEL_EDIT,
    ADMIN_INTERACTION_LEVEL,
    DISABLED_DISPLAY_TEXT,
)

from typing import Type
import warnings, inspect

_registry: set["RegisteredBlock"] = set()


def get_module_path(obj):
    module = inspect.getmodule(obj)
    return module.__name__


def get_sorted_registry():
    """
        Gets the registry and sorts it by the import path.
        Also sets the is_shown attribute to True or False based on the backend.
    """
    registry = copy.deepcopy(_registry)
    registry = sorted(registry, key=lambda block: block.import_path)

    backend = get_showable_backend()
    registry_data = backend.registry_data()
    if not registry_data:
        return registry
    
    for block in registry:
        block.is_shown = registry_data.get(block.import_path, False)

    return registry

class RegisteredBlock:
    def __init__(self, 
            block: blocks.Block = None,
            label: str          = None,
            help_text: str      = None,
        ):
        self.block = block
        self.label = label
        self.help_text = help_text
        self.module = get_module_path(block)
        self.import_path = f"{self.module}.{block.__name__}"
        self.is_shown = False # This is set by the backend

    def __hash__(self):
        return hash(self.block)

    def __eq__(self, other):
        if not isinstance(other, RegisteredBlock):
            return self.block == other
        return self.block == other.block


def get_registry_form():
    class RegistryForm(forms.Form):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            for block in get_sorted_registry():
            
                self.fields[block.import_path] = forms.BooleanField(
                    label=block.label,
                    help_text=block.help_text,
                    initial=block.is_shown,
                    required=False,
                )

        def to_dict(self):
            return {k: v for k, v in self.cleaned_data.items()}

    return RegistryForm

_css_class = "wagtail-showables-disabled"

if ADMIN_INTERACTION_LEVEL == ADMIN_INTERACTION_LEVEL_NONE:
    _css_class += " wagtail-showables-no-interaction"
elif ADMIN_INTERACTION_LEVEL == ADMIN_INTERACTION_LEVEL_SHOW:
    _css_class += " wagtail-showables-show-interaction"
elif ADMIN_INTERACTION_LEVEL == ADMIN_INTERACTION_LEVEL_EDIT:
    _css_class += " wagtail-showables-edit-interaction"


def register_block(block: Type[blocks.StructBlock] = None, label: str = None, help_text: str = None):
    if block is None:
        return lambda block: register_block(block, label, help_text)
        
    if not issubclass(block, blocks.StructBlock):
        raise ValueError(f"{block} is not a subclass of wagtail.blocks.StructBlock, this is required for wagtail_showables.")
    
    if block in _registry:
        raise ValueError(f"{block} is already registered")

    # Override the render method and render form method
    # Block must not be shown to the users if admin says it is hidden.
    # We will display to the admin which blocks are hidden by wrapping it in a simple div.
    # clean = block.clean
    render = block.render
    render_form_template = block.render_form_template

    backend = get_showable_backend()

    # def 

    def render_if_shown(self: blocks.StructBlock, value, context=None):
        backend.renew()
        if not backend.is_shown(
            f"{get_module_path(self)}.{self.__class__.__name__}",
        ):
            return ""
        return render(self, value, context)
    
    def wrap_if_hidden(self: blocks.StructBlock):
        rendered = render_form_template(self)

        backend.renew()

        if not backend.is_shown(
            f"{get_module_path(self)}.{self.__class__.__name__}",
        ):
            rendered = f'<div class="{_css_class}" style="--disabled-text: \'{escape(DISABLED_DISPLAY_TEXT)}\';">{rendered}</div>'
        return rendered

    block.render = render_if_shown
    block.render_form_template = wrap_if_hidden
    
    if hasattr(block, "meta"):
        block.meta.form_template = "wagtail_showables/block_form_template.html"
    elif hasattr(block, "Meta"):
        if not hasattr(block.Meta, "form_template"):
            block.Meta.form_template = "wagtail_showables/block_form_template.html"
        else:
            warnings.warn(f"block.Meta.form_template is already set to {block.Meta.form_template}")
    else:
        if getattr(block._meta_class, "form_template", None):
            warnings.warn(f"block._meta_class().form_template is already set to {block._meta_class.form_template}")
        else:
            class Meta:
                form_template = "wagtail_showables/block_form_template.html"

            meta_class_bases = [block._meta_class, Meta] + [
                getattr(base, "_meta_class", None) for base in block.__bases__
            ]
            meta_class_bases = tuple(filter(bool, meta_class_bases))
            block._meta_class = type(str(block.__name__ + "Meta"), meta_class_bases, {})

    _registry.add(RegisteredBlock(
        block=block,
        label=label,
        help_text=help_text,
    ))

    return block

