from mesa import Agent
from mesa.model import Model 

class TrashBinAgent (Agent):
    def __init__(self, unique_id: int, model: Model) -> None:
        super().__init__(unique_id, model)

        self.trash = 0
        
    def step(self) -> None:
        pass