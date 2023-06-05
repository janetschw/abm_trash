from typing import Any
from mesa import Model



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