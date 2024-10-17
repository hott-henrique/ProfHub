from api.control.CentralController import CentralController

global G

G = dict()

def get_controller():
    global G

    controller = G.get("CENTRAL_CONTROLLER", None)

    if controller is None:
        controller = G["CENTRAL_CONTROLLER"] = CentralController()

    return controller
