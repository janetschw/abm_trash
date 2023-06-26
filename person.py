from mesa import Agent
from mesa.model import Model
from trash_bin import TrashBinAgent
from trash import TrashAgent

class PersonAgent(Agent):
    def __init__(self, unique_id: int, model: Model, pos, view_range, awareness, messiness) -> None:
        super().__init__(unique_id, model)
        self.pos = pos
        self.view_range = round(self.random.gauss(view_range, 1))
        self.awareness = round(self.random.gauss(awareness, 1))
        self.messiness = round(self.random.gauss(messiness, 1))
        self.trash = self.random.randint(0, 4)
        self.frustration = 0
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
        if self.destination is not None:
            self.collect_trash()
        else:
            self.drop_trash()
        self.move()
        if self.trash > 0:
            self.frustration += 1
        self.create_trash()
        self.dispose_trash()
        

    def spot_trash_bins(self):
        if self.trash > 0:
            neighbors = self.model.grid.get_neighbors(
                pos = self.pos, moore = True, include_center = True, radius = self.view_range
            )
            #jetzt wes er wer um ihn rum steht 
            for agentneighbor in neighbors:
                if isinstance(agentneighbor, TrashBinAgent):
                    self.destination = agentneighbor.pos
                    break

    def collect_trash(self):
        if self.awareness > self.random.randint(0,10):
            neighbors = self.model.grid.get_neighbors(
                pos = self.pos, moore = True, include_center = True, radius = 1
            )
            for agentneighbor in neighbors:
                if isinstance(agentneighbor, TrashAgent):
                    self.model.grid.remove_agent(agentneighbor)
                    self.trash += 1

    def drop_trash(self):
        if self.trash > 0 and self.frustration > self.awareness:
            new_trash = TrashAgent(model=self.model, unique_id=self.model.next_id())
            self.model.grid.place_agent(new_trash, self.pos)
            self.trash = 0
            self.frustration = 0

    def create_trash(self):
        if self.messiness > self.random.randint(0, 10):
            self.trash += 1

    def dispose_trash(self):
        if self.trash > 0:
            neighbors = self.model.grid.get_neighbors(
                pos = self.pos, moore = True, include_center = True, radius = 1
            )
            for agentneighbor in neighbors:
                if isinstance(agentneighbor, TrashBinAgent):
                    agentneighbor.trash += self.trash
                    self.trash = 0
                    self.frustration = 0
                    self.destination = None

    # def step(self)   
    #     for TrashAgent in self.TrashAgent(shuffled=False):
    #         agent.step()
    #     self.steps += 5
    #     self.time += 5
    
    # def get_TrashAgent_count(self) -> int:
    #      return 
            

#TrashAgent soll von PersonAgent erkannt werden
#TrashAgent soll von PersonAgent geadded werden 
#TrashAgent soll die selben Schritte gehen wie PersonAgent (maximal 5 Schritte)
#TrashAgent soll nach 5 Schritten fallen gewerden lassen oder vor 5 Schritten in die TrashBin geschmissen wreden, wenn vorhande 



    
