from mesa import Agent
from mesa.model import Model
from trash_bin import TrashBinAgent
from trash import TrashAgent
from pub import PubAgent

# Hier werden die Personen (Person agents) definiert die in unserem Modell rumlaufen und welche aktionen diese ausführen 

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
        self.dest_is_trash_bin = False

    # Dies sind alles die Eigenschaften die der/die Agent haben soll 

    #In den nachfolgenden Zeilen wird definiert wie genau sich ein Agent bewegt und wie er seine Strecke bestimmt 
    def move(self):
        if self.destination is None:
            self.pick_random_destination()

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
            # neighborhood = self.model.grid.get_neighborhood(
            #     pos = self.pos, moore = True, include_center = False, radius = 1
            # )
            # #hier wird die position ausgwewählt
            # targetpos = self.random.choice(neighborhood)
            # self.model.grid.move_agent(agent = self, pos = targetpos)

    def step(self):
        self.spot_trash_bins()
        if self.dest_is_trash_bin:
            self.collect_trash()
        else:
            self.drop_trash()
        self.move()
        if self.trash > 0:
            self.frustration += 1
        self.create_trash()
        self.dispose_trash()
        self.am_i_there()
        
     # Was passiert wenn Müll (trash) entdeckt wird 
    
    def spot_trash_bins(self):
        if self.trash > 0:
            neighbors = self.model.grid.get_neighbors(
                pos = self.pos, moore = True, include_center = True, radius = self.view_range
            )
            #jetzt wes er wer um ihn rum steht 
            for agentneighbor in neighbors:
                if isinstance(agentneighbor, TrashBinAgent):
                    self.destination = agentneighbor.pos
                    self.dest_is_trash_bin = True
                    break

    #Hier wird progammiert was passiert wenn der Müll aufgesammlet wird in dem Moment wenn ein Agent an diesem vorbei oder drüber läuft
    
    def collect_trash(self):
        if self.awareness > self.random.randint(0,10):
            neighbors = self.model.grid.get_neighbors(
                pos = self.pos, moore = True, include_center = True, radius = 1
            )
            for agentneighbor in neighbors:
                if isinstance(agentneighbor, TrashAgent):
                    self.model.grid.remove_agent(agentneighbor)
                    self.trash += 1
                    self.model.total_trash -= 1

    # Wann lässt der Agent seinen Müll fallen?
    
    def drop_trash(self):
        if self.trash > 0 and self.frustration > self.awareness:
            for i in range(self.trash):
                new_trash = TrashAgent(model=self.model, unique_id=self.model.next_id())
                self.model.grid.place_agent(new_trash, self.pos)
                self.model.total_trash += 1
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
                    self.dest_is_trash_bin = False

    # Wie bewegt sich der GAnt und wie wählt er sin Ziel?
    
    def pick_random_destination(self):
        cell = self.random.choice(list(self.model.grid.coord_iter()))
        pos = cell[1:]
        self.destination = pos
        self.dest_is_trash_bin = False

    # Der Agent überprüft an welcher stelle er sich befindet
    
    def am_i_there(self):
        if self.pos == self.destination:
            self.destination = None

    # def spot_pub (self):
    #     if self.trash == 0:
    #         neighbors = self.model.grid.get_neighbors(
    #             pos = self.pos, moore = True, include_center = True, radius = 1
    #         )
    #         for agentneighbor in neighbors:
    #             if isinstance(agentneighbor, PubAgent):
    #                 agentneighbor.pub += self.pub
    #                 self.trash = 0
    #                 self.frustration = 0
    #                 self.destination = None


    
