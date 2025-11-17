from skfuzzy import control as ctrl

_controller = None

def get_fuzzy_sim():
    global _controller
    if _controller is None:
        from .rules import build_fuzzy_controller
        _controller = ctrl.ControlSystem(build_fuzzy_controller().rules)
    return ctrl.ControlSystemSimulation(_controller)
