wagtail_showables
=================

An application to easily toggle types of blocks on your frontend from being seen.

It can also be used to limit admins in what they can see and edit - though there is no validation for this due to limitations with wagtail.

Quick start
-----------

1. Add 'wagtail_showables' to your `INSTALLED_APPS` setting like this:

   ```
   INSTALLED_APPS = [
   ...,
   'wagtail_showables',
   ]
   ```
2. Add the middleware to your `MIDDLEWARE` to allow for high-performance operations.

   ```python
   MIDDLEWARE = [
       "wagtail_showables.middleware.ShowablePerformanceDataMiddleware",
   ]

   ```
3. Set the default backend setting `WAGTAIL_SHOWABLES_DEFAULT_BACKEND`

   ```python
   WAGTAIL_SHOWABLES_DEFAULT_BACKEND = "performance_db"
   ```
4. Run `python manage.py migrate` to create the wagtail_showables models.
5. Run `python manage.py collectstatic` to collect the wagtail_showables static files.

## Options



### WAGTAIL_SHOWABLES_ADMIN_INTERACTION_LEVEL

The level of which the editor can interact with the block.
Options are:

```python
0 # Completely disabled and blurred out from viewing.
1 # Disabled from editing.
2 # Fully enabled
```

Example:

```python
WAGTAIL_SHOWABLES_ADMIN_INTERACTION_LEVEL = 2 # Admins can edit this block.
```

### WAGTAIL_SHOWABLES_DISABLED_DISPLAY_TEXT

The text to display when the block is disabled.
This only has an effect with `ADMIN_INTERACTION_LEVEL` set to 0.
Example:

```python
WAGTAIL_SHOWABLES_DISABLED_DISPLAY_TEXT = "This block is currently disabled."
```

### WAGTAIL_SHOWABLES_DEFAULT_BACKEND

The default backend to use for the showables.
Options are:

```python
"default" # Uses the default backend (caches, but refreshes way more often than the other backends.)
"performance_db" # Uses the database to store the showable data.
"performance_cache" # Uses the cache to store the showable data.
```

## Registering blocks with Wagtail Showables

To register a block with Wagtail Showables, you simply import the register function:

```python
from wagtail_showables.registry import register_block
```

Then, you can use the function to register your block:

```python
# def register_block(block: Type[blocks.StructBlock] = None, label: str = None, help_text: # str = None):

class MyBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    content = blocks.RichTextBlock()

register_block(MyBlock, label="My Block", help_text="This block gets used in application X and does Y.")
```

It can also be used as a decorator:

```python
@register_block(label="My Block", help_text="This block gets used in application X and does Y.")
class MyBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    content = blocks.RichTextBlock()
```

You are now set to enable and disable blocks from the admin and users.

Simply head to the admin area, open the settings menu and go to the Showable Blocks menu.
