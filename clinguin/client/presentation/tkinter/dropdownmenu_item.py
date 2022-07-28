import tkinter as tk

from .root_cmp import RootCmp
from .call_back_definition import CallBackDefinition

class DropdownmenuItem(RootCmp):

    def _defineComponent(self, elements):
        menu = elements[str(self._parent)][0]
        return menu

    def _defineStandardAttributes(self, standard_attributes):
        standard_attributes["label"] = {"value":"", "exec":self._empty}

    def _empty(self, component, key, standard_attributes):
        pass

    def _defineActions(self, actions):
        actions["click"] = {"policy":None, "exec":self._defineClickEvent}


    def _defineClickEvent(self, component, key, actions, standard_attributes, special_attributes, elements):
        if actions[key]:
            component['menu'].add_command(
                label=standard_attributes["label"]["value"],
                command=CallBackDefinition(
                    self._id,
                    self._parent,
                    actions[key]['policy'],
                    elements,
                    self._dropdownmenuitemClick))

    def _dropdownmenuitemClick(self, id, parent, click_policy, elements):
        variable = elements[str(parent)][1]["variable"]
        variable.set(id)
        if (click_policy is not None):
            self._base_engine.assume(click_policy)
















