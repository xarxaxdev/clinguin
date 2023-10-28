"""
Module that contains the Temporal Backend.
"""

from clingo import parse_term
from clingo.script import enable_python
from clingo.symbol import Function, Number

# Self defined
from clinguin.server.application.backends.clingo_multishot_backend import ClingoMultishotBackend

enable_python()


class TemporalBackend(ClingoMultishotBackend):
    """
    TODO -> Add documentation!
    """

    def __init__(self, args):
        super().__init__(args)

        self._step = 1
        self._last_grounded_step = 0
        self._full_plan = None
        self._model = None

    def _init_ctl(self):
        self._step = 1
        self._last_grounded_step = 0
        self._full_plan = None
        super()._init_ctl()

    def _ground(self):
        if not self._last_grounded_step:
            self._ctl.ground([("base", [])])
        while self._step > self._last_grounded_step:
            self._last_grounded_step += 1
            self._ctl.ground([("step", [Number(self._step)])])
        if self._step > 1:
            self._ctl.assign_external(
                Function("query", [Number(self._step - 1)]), False
            )
        self._ctl.assign_external(Function("query", [Number(self._step)]), True)

    def _find_incrementally(self):
        if self._step > 1:
            self._ctl.assign_external(
                Function("check", [Number(self._step - 1)]), False
            )
        self._ctl.assign_external(Function("check", [Number(self._step)]), True)
        plan = self._find_plan()

        while plan is None or self._step > 100:
            self._step += 1
            self._ground()
            if self._step > 1:
                self._ctl.assign_external(
                    Function("check", [Number(self._step - 1)]), False
                )
            self._ctl.assign_external(Function("check", [Number(self._step)]), True)
            plan = self._find_plan()

        if self._full_plan is None:
            raise RuntimeError("No plan found before 100 steps")

        return self._full_plan

    def _find_plan(self):
        self._ctl.configuration.solve.enum_mode = "auto"
        hdn = self._ctl.solve(
            assumptions=[(a, True) for a in self._assumptions], yield_=True
        )
        itr = iter(hdn)
        try:
            model = next(itr)
            self._full_plan = model.symbols(atoms=True)
            hdn.cancel()
        except StopIteration:
            hdn.cancel()
            self._full_plan = None

        return self._full_plan

    def find_plan(self):
        """
        TODO -> Add documentation!
        """
        if not self._full_plan:
            self._find_incrementally()

        symbols = "\n".join([str(s) + "." for s in self._full_plan])
        wctl = self._uifb.ui_control(extra_ui_prg=symbols)
        self._model = self._uifb.from_ctl(wctl)
        self._update_uifb()

    def assume_and_step(self, predicate):
        """
        TODO -> Add documentation!
        """
        predicate_symbol = parse_term(predicate)
        self._add_assumption(predicate_symbol)
        self._step += 1
        self._ground()
        self._end_browsing()
        self._update_uifb()

    def remove_assumption(self, predicate):  # pylint: disable=W0613
        """
        TODO -> Add documentation!
        """
        raise NotImplementedError()

    def next_solution(self, opt_mode=None):  # pylint: disable=W0613
        """
        TODO -> Add documentation!
        """
        raise NotImplementedError()
