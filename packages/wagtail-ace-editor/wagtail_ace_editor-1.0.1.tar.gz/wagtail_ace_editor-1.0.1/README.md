wagtail_ace_editor
==================

Wagtail Ace Editor is a simple extension which provides access to the [Ace Editor Library](https://github.com/ajaxorg/ace).

Usage is simple and easy like you're used to from any django widget.

We provide a custom theme based on the default cobalt theme to fit into your wagtail application - this is the default theme.

The full library from [Ace Editor on UNPKG](https://unpkg.com/ace-builds@1.3.3/src-min/) has been included to be used.

## Note

This widget is only for use in the wagtail's admin area - it does not do anything for your frontend. 

If demand for this appears to be high in the future it will be added.

Quick start
-----------

1. Add 'wagtail_ace_editor' to your INSTALLED_APPS setting like this:

   ```
   INSTALLED_APPS = [
   ...,
   'wagtail_ace_editor',
   ]
   ```
2. Run `py manage.py collectstatic` to collect all the relevant javascript and css files.
3. Simply import the widget, or blocks into your django application and use them!

   ```python
   from wagtail_ace_editor.blocks import AceEditorBlock
   from wagtail_ace_editor.widgets import AceEditorWidget
   # Formfield: from wagtail_ace_editor.forms import AceEditorField

   # ... other imports

   class MyModel(models.Model):
       	html_field = models.TextField(
   		...
   	)

   	content = StreamField([
   		('html_block', AceEditorBlock(
   		    # Mode to use for your ace editor.
   		    mode="ace/mode/django"
   		    # Theme to use for your ace editor.
   		    theme="ace/theme/wagtail",
   		    # Include parent template context when using wagtail's {% include_block %} method.
   		    include_template_context: bool

   		    # Render ace/mode/(html-django) inside of an iFrame as opposed to escaping it.
   		    use_frame_preview: bool

   		    # When using ace/mode/(html-django), allows you to pass in custom CSS to style the iFrame
   		    frame_css: list[str]

   		    # When using ace/mode/(html-django), allows you to pass in custom JS to script inside of iFrame
   		    frame_js: list[str]
   		)),
    	])

   	panels = [
   		FieldPanel("html_field", widget=AceEditorWidget(
   			use_frame_preview: bool
   			frame_css: list[str]
   			frame_js: list[str]
   		)),
   		FieldPanel("content"),
   	]

   ```
