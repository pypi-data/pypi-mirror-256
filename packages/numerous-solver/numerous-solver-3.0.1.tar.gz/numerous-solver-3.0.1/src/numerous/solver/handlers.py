from .interface import Interface
from .solve_states import SolveEvent
from .base import Solution, SolverInfo
from .events import StateEvent, TimeEvent
from typing import List, Dict
from abc import ABC, ABCMeta, abstractmethod

class EventHandler(ABC):
    """Event handler abstract class. Used to create event handlers for numerous solver.

    :param state_events: a list of all state events
    :param interface: model interface

    """
    state_events: Dict[str, StateEvent]
    time_events: Dict[str, TimeEvent]
    external_events: Dict[str, StateEvent | TimeEvent]
    interface: Interface



    def __init_subclass__(cls, **kwargs):
        __protected_methods__ = ["set_solver_interface_and_events", "trigger_external_events", "handle_solve_event"]
        super().__init_subclass__(**kwargs)
        for method_name in cls.__dict__:
            if method_name in __protected_methods__:
                raise TypeError(f"Cannot override protected method {method_name} in {cls.__name__}")

    def set_solver_interface_and_events(self,

                 state_events: Dict[str, StateEvent],
                 time_events: Dict[str, TimeEvent],
                 external_events: Dict[str, StateEvent | TimeEvent],
                 interface: Interface
                 ):
        """
        Method called after solver has created interface and compiled events. Sets properties necessary for handling
        all events that occur in the outer loop.

        """

        self.state_events = state_events
        self.time_events = time_events
        self.external_events = external_events
        self.interface = interface

    def trigger_external_events(self, info: SolverInfo, t: float, events: Dict[str, TimeEvent | StateEvent]):

        y = self.interface.get_states()
        direction = info.direction
        external_events = [event for event in events.values() if event.is_external()]
        for event in external_events:
            if event.is_triggered():
                external_event = self.external_events[event.id]
                y = external_event.run_event_action(self.interface, t, y)
                external_event.post_event(self.interface, direction, t, y)
                event.clear()
                self.interface.set_states(y)

    @abstractmethod
    def post_init(self, t0: float):
        """
        Method called after initialization of solver
        """
        pass

    def handle_solve_event(self, info: SolverInfo, t: float):
        """Method called each time the solver exits its inner loop

        :param info: The solver info object holding the solution, along with event id, returned from the solver
        :type info: :class:`solver.base.SolverInfo`
        :param t: current solver time
        :type t: float
        :return:
        """

        event_id = info.event_id

        if event_id == SolveEvent.Historian:
            return self.handle_external_historian_update(info, t)
        elif event_id == SolveEvent.ExternalDataUpdate:
            return self.handle_external_data_update(info, t)
        elif event_id == SolveEvent.HistorianAndExternalUpdate:
            self.handle_external_historian_update(info, t)
            return self.handle_external_data_update(info, t)
        elif event_id == SolveEvent.TimeEvent:
            self.trigger_external_events(info, t, self.time_events)
            return self.handle_post_external_time_event(info, t)
        elif event_id == SolveEvent.StateEvent:
            self.trigger_external_events(info, t, self.state_events)
            return self.handle_post_external_state_event(info, t)

    @abstractmethod
    def handle_external_historian_update(self, info: SolverInfo, t: float):
        """
        Method called when the external historian needs to be updated. Must be specified by user.

        :param interface: model interface
        :type interface: :class:`solver.interface.Interface`
        :param info: The solver info object holding the solution, along with event id, returned from the solver
        :type info: :class:`solver.base.SolverInfo`
        :param t: current solver time

        """

        pass

    @abstractmethod
    def handle_external_data_update(self, info: SolverInfo, t: float):
        """
        Method called when external data needs to be updated. Must be specified by user.

        :param interface: model interface
        :type interface: :class:`solver.interface.Interface`
        :param info: The solver info object holding the solution, along with event id, returned from the solver
        :type info: :class:`solver.base.SolverInfo`
        :param t: current solver time

        """

        pass

    @abstractmethod
    def handle_post_external_time_event(self, info: SolverInfo, t: float):
        """
        Method called after external time events have run. Must be specified by user.

        :param interface: model interface
        :type interface: :class:`solver.interface.Interface`
        :param info: The solver info object holding the solution, along with event id, returned from the solver
        :type info: :class:`solver.base.SolverInfo`
        :param t: current solver time

        """

        pass

    @abstractmethod
    def handle_post_external_state_event(self, info: SolverInfo, t: float):
        """
        Method called after external state events have run. Must be specified by user.

        :param interface: model interface
        :type interface: :class:`solver.interface.Interface`
        :param info: The solver info object holding the solution, along with event id, returned from the solver
        :type info: :class:`solver.base.SolverInfo`
        :param t: current solver time

        """

        pass

    @abstractmethod
    def reset_solution(self):
        """Method called when resetting the solution. Must be implemented by user.

        :return:
        """
        pass


class DefaultEventHandler(EventHandler):
    def __init__(self):
        self.solution = Solution()

    def handle_post_external_state_event(self, info: SolverInfo, t:float):
        self.solution.add_state_event_result(t, self.interface.get_states())

    def handle_post_external_time_event(self, info: SolverInfo, t: float):
        self.solution.add_time_event_result(t, self.interface.get_states())

    def handle_external_historian_update(self, info: SolverInfo, t: float):
        self.solution.add_result(t, self.interface.get_states())

    def handle_external_data_update(self, info: SolverInfo, t: float):
        pass

    def post_init(self, t0: float):
        self.solution.add_result(t0, self.interface.get_states())

    def reset_solution(self):
        """Default method for resetting solution

        :return:
        """
        self.solution.reset()
