# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Button(Component):
    """A Button component.
SSB styled Button for triggering actions

Keyword arguments:

- children (optional):
    Button text or/and icon.

- id (optional)

- ariaLabel (default '')

- className (default ''):
    Optional container class.

- disabled (default False):
    Decides if the button is disabled.

- icon (optional):
    Renders an icon.

- n_clicks (default 0):
    Number of times the button has been clicked.

- negative (default False):
    Changes design.

- primary (default False):
    Changes style to represent a primary button.

- setProps (optional):
    Dash-assigned callback that should be called to report property
    changes to Dash, to make them available for callbacks.

- type (default 'button'):
    Button type. Can be 'submit', 'reset', or 'button'. Defaults to
    'button'."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'ssb_dash_components'
    _type = 'Button'
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, n_clicks=Component.UNDEFINED, className=Component.UNDEFINED, disabled=Component.UNDEFINED, icon=Component.UNDEFINED, negative=Component.UNDEFINED, primary=Component.UNDEFINED, type=Component.UNDEFINED, ariaLabel=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'ariaLabel', 'className', 'disabled', 'icon', 'n_clicks', 'negative', 'primary', 'setProps', 'type']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'ariaLabel', 'className', 'disabled', 'icon', 'n_clicks', 'negative', 'primary', 'setProps', 'type']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(Button, self).__init__(children=children, **args)
