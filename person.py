from mesa import Agent
from mesa.model import Model
from trash_bin import TrashBinAgent

class PersonAgent(Agent):
    def __init__(self, unique_id: int, model: Model, pos) -> None:
        super().__init__(unique_id, model)
        self.pos = pos
        self.view_range = 5
        self.destination = None

    def move(self):
        if self.destination is not None:
            dir_x = self.destination[0] - self.pos[0]
            dir_y = self.destination[1] - self.pos[1]
            x = 0
            y = 0
            if dir_x < 0:
                x = -1
            elif dir_x > 0:
                x = 1

            if dir_y < 0:
                y = -1
            elif dir_y > 0:
                y = 1
            new_pos = (self.pos[0] + x, self.pos[1] + y)
            self.model.grid.move_agent(agent = self, pos = new_pos)
        else:
            neighborhood = self.model.grid.get_neighborhood(
                pos = self.pos, moore = True, include_center = False, radius = 1
            )
            #hier wird die position ausgwewählt
            targetpos = self.random.choice(neighborhood)
            self.model.grid.move_agent(agent = self, pos = targetpos)

    def step(self):
        self.spot_trash_bins()
        self.move()

    def spot_trash_bins(self):
        neighbors = self.model.grid.get_neighbors(
            pos = self.pos, moore = True, include_center = True, radius = self.view_range
        )
        #jetzt wes er wer um ihn rum steht 
        for agentneighbor in neighbors:
            if isinstance(agentneighbor, TrashBinAgent):
                self.destination = agentneighbor.pos
                break


    
