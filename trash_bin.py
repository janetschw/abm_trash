from mesa import Agent
from mesa.model import Model
from trash import TrashAgent

# Hier wird der mülleimer (TrashbinAgent) definiert. 
# Seine Eigenschaften werden hinzugefügt (self.)

class TrashBinAgent (Agent):
    def __init__(self, unique_id: int, model: Model, capacity: int, pickup_interval: int, pos) -> None:
        super().__init__(unique_id, model)
        self.pos = pos # Postion
        self.trash = self.random.randint(0, capacity)
        self.capacity = capacity # Füllmenge
        self.pickup_interval = pickup_interval # Wie oft wird der Müll geleert
        self.steps_since_last_pickup = 0 # Wie lange ist die letzte entleerung her?

    # Was "denkt" der Mülleimer bei jedem schritt in welcher Reihenfolge
    
    def step(self):
        if self.trash > self.capacity:
            self.drop_trash()
        self.steps_since_last_pickup += 1
        if self.steps_since_last_pickup > self.pickup_interval:
            self.dispose_trash()

    # Wann lässt der Mülleimer Müll in den Felder um sich herrum fallen? 
    def drop_trash(self):
        excess_trash = self.trash - self.capacity #wenn er voll ist 
        for i in range(excess_trash):
            new_trash = TrashAgent(model=self.model, unique_id=self.model.next_id())
            pos = self.random.choice(self.model.grid.get_neighborhood(self.pos, True, False, 1))
            self.model.grid.place_agent(new_trash, pos)
            self.model.total_trash += 1
            
        # Müll wird zum Grid hinzugefügt
        
        self.trash = self.capacity

    def dispose_trash(self):
        self.trash = 0
        self.steps_since_last_pickup = 0
        neighbors = self.model.grid.get_neighbors(
            pos = self.pos, moore = True, include_center = False, radius = 1
        )
        for agentneighbor in neighbors:
            if isinstance(agentneighbor, TrashAgent):
                self.model.grid.remove_agent(agentneighbor)
                self.model.total_trash -= 1
