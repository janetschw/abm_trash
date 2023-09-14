import mesa
from field import Kiez 
from person import PersonAgent 
from trash import TrashAgent
from trash_bin import TrashBinAgent
from pub import PubAgent

# Wie sehen unsere verschiedenen Agenten aus

def draw(agent):
    if agent is None:
        return 
    
    if isinstance(agent, PersonAgent): # der Agent ist eine Person
        color = "#57F828"
        if agent.trash > 0:
            color = "#F6DA30"
        if agent.frustration > agent.awareness:
            color = "#F53334"
        return {
            "Color": color,
            "Shape": "circle", # Form des Agenten
            "Layer": 1,        # Auf welcher Ebene bewegt sich dieser
            "Filled": "false", # Ist die Form des Agenten gefüllt oder nicht?
            "r": 0.5           # Größe des Agenten 
        }
    
    if isinstance(agent, TrashAgent): # Der Agent ist der Müll 
        return {
            "Color": "rgba(0,0,0,0.1)",   # Farbcode
            "Shape": "rect",
            "Layer": 0,
            "Filled": "true",
            "w": 0.5,
            "h": 0.5
        }
    
    if isinstance(agent, TrashBinAgent): # Der Agent ist der Mülleimer
        text_color = "#57F828"
        if agent.trash >= 0.8 * agent.capacity:
            text_color = "#F6DA30"
        if agent.trash >= agent.capacity:
            text_color = "black"
        return {
            "Color": "red",
            "Shape": "rect",
            "Layer": 0,
            "Filled": "true",
            "w": 1,
            "h": 1,
            "text": (agent.trash, agent.capacity)[agent.trash >= agent.capacity],
            "text_color": text_color
        }
    
    if isinstance(agent, PubAgent): # Der Agent ist der Pub/Laden
        return {
            "Color": "rgba(0,0,0,0.1)",
            "Shape": "rect",
            "Layer": 0,
            "Filled": "true",
            "w": 1,
            "h": 1
        }
    
    
canvas = mesa.visualization.CanvasGrid(draw, 40, 40, 600, 600)
model_params = {
    "num_persons": mesa.visualization.Slider("num_persons", 20, 0, 100, 1),
    "num_trash": mesa.visualization.Slider("num_trash", 30, 0, 200, 1),
    "num_trash_bins": mesa.visualization.Slider ("num_trash_bins", 5, 0, 20, 1),
    "messiness": mesa.visualization.Slider ("messiness", 5, 0, 10, 1),
    "awareness": mesa.visualization.Slider ("awareness", 5, 0, 10, 1),
    "view_range": mesa.visualization.Slider ("view_range", 5, 0, 10, 1),
    "trash_bin_capacity": mesa.visualization.Slider("trash_bin_capacity", 20, 5, 50, 1),
    "pickup_interval": mesa.visualization.Slider("pickup_interval", 30, 5, 50, 1)
}

# set charts to visualize the development of the model
# "Label" must correspond to a model_reporter set in model.py
trash_charts = mesa.visualization.ChartModule([
    {"Label": "Littering", "Color": "grey"}
])

# # function that is called every step for every field and every agent to decide how it should be displayed
# def draw(agent):
#     # if there is no agent on a field
#     # return nothing
#     if agent is None:
#         return

#     # else create a "portrayal" object (dictionary) with the needed parameters
#     # casing (lower or upper case letters are always important!)
#     # we define a standard portrayal that is used by default for all agents
#     # in a dictionary every "key" has a "value" ({"key": "value"})
#     # an individual value of a dictionary can be accessed by specifiying the "key" you want to read the "value" for
#     # portrayal["Color"] -> "blue"
#     # see https://www.w3schools.com/python/python_dictionaries.asp
#     portrayal = {
#         "Color": "blue",
#         "Shape": "circle",
#         "Layer": 0,
#         "Filled": "true", # here the boolean (True, False) value is given as a string (text), this is not the default in Python!
#         "r": 0.5 # radius of the circle
#     }

#     # if the agent is a mangrove though, we overwrite the variable portrayal
#     # so far all agents are Mangroves, so the default will never be used
#     if isinstance(agent, Mangrove):
#         portrayal = {
#             # "green" in RGBA looks like that: "rgba(0, 128, 0, 1)""
#             # values have to be between 0 and 255, transparency 0 to 1
#             # make the color green, but more transparent when health decreases
#             # use "abs" (absolute value) and "round" to make sure the number is positive and one digit decimal
#             "Color": "rgba(0, 128, 0, {})".format(abs(round(agent.health, 1))),
#             "Shape": "rect",
#             "Layer": 0,
#             "Filled": "true",
#             "w": 1, # height of the field
#             "h": 1 # 
#         }
#     # use another "if" or "elif" (else if) to check another agent type, or any other property
#     # e.g.: elif isinstance(agent, Trash): ...
#     # instead of defining the default portrayal above,
#     # you can also use "else" in the end to set the portrayal if no condition before was met

#     # return the portrayal that has been set
#     return portrayal

# # initialize the canvas to draw on with a size in fields and pixels
# canvas = mesa.visualization.CanvasGrid(draw, 40, 40, 600, 600)

# # Sliders for modifiying parameters going into the model
# # parameters must be defined in the constructor of the model
# # those will overwrite the defaults set in the model constructor
# # read what the numbers mean by hovering with the cursor above the "Slider"
# model_params = {
#     "mangrove_fertility": mesa.visualization.Slider("Mangrove fertility", 0.1, 0, 1, 0.05),
#     "mangrove_life_expectancy": mesa.visualization.Slider("Mangrove Life Expectancy", 10, 0, 20, 1),
#     "mangrove_density": mesa.visualization.Slider("Mangrove Density", 0.15, 0, 1, 0.05)
# }

# # initialize the server with the model, parameters and visualization elements set above
# # give it a name of your choosing
server = mesa.visualization.ModularServer(
    model_cls=Kiez,
    visualization_elements=[canvas, trash_charts],
    name="Kiez Modell",
    model_params=model_params
)
