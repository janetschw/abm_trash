import mesa
from model import Kiez 
from person import PersonAgent

def draw(agent):
    if agent is None:
        return
    
    if isinstance(agent, PersonAgent):
        return {
            "Color": "blue",
            "Shape": "circle"                    
                 
                 
                      }

    canvas = mesa.visualization.CanvasGRid(draw, 40, 40, 600, 600)
    model_params = {
        "num_persons": mesa.visualization("num_persons", 20, 0, 100, 1),
        "num_trash":  mesa.visualization(),
        "num_trash_bins":  mesa.visualization(),
        "messiness":  mesa.visualization(),
        "awareness":  mesa.visualization(),
        "view_range":  mesa.visualization()
    }

    server =  mesa.visualization.ModularServer()