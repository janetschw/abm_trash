from mesa import Model
from mesa.time import RandomActivation



class Kiez(Model):
    num_persons: int
    num_trash_bins: int
    num_trash: int 
    messiness: int
    awareness: int
    view_range: int 
    #current_time: int 
    #pickup_time: int 

    def __init__(self,num_persons,num_trash_bins,num_trash,messiness,awareness,view_range) -> None:
        super().__init__()

        self.num_persons = 30 

        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(40, 40, False)

        self.spawn_trash()
        self.spawn_persons()
        self.spawn_trash_bins ()

    def spawn_trash():
        return None 
    
    def spawm_persons():
        return None
    
    def spawn_trash_bins():
        return None