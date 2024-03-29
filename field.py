from mesa import Model, DataCollector
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from person import PersonAgent
from trash import TrashAgent
from trash_bin import TrashBinAgent

#Alle benötigten Daten werden ins Feld importiert damit alles vom Programm gelesen und verstanden werden kann  
#von isabelle: from pub import PubAgent
class Kiez(Model):
    grid: MultiGrid
    num_persons: int
    num_trash_bins: int
    num_trash: int 
    messiness: int
    awareness: int
    view_range: int 
    total_trash: int
#von isabelle: num_pub: int 
    def __init__(
            self,
            num_persons,
            num_trash_bins,
            num_trash,
            messiness,
            awareness,
            view_range,
            trash_bin_capacity,
            pickup_interval
        ) -> None:
        super().__init__()

            #alle parameter werden festgelegt
#von isabelle: def__int__ um auch die Attribute des pubs zu initialisieren also num_pubs,pub_trash_capacity,pub_person_capacity, neue attribut für person_agents bsp. trinklust welche random festgelegt werden sollen und wahrscheinlichkeit der destination zum pubagent beeinflusst 
        self.num_persons = num_persons
        self.num_trash_bins = num_trash_bins
        self.messiness = messiness
        self.awareness = awareness
        self.view_range = view_range
        self.num_trash = num_trash
        self.trash_bin_capacity = trash_bin_capacity
        self.pickup_interval = pickup_interval
        self.total_trash = 0

        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(40, 40, False)
        
        self.spawn_persons()
        self.spawn_trash()
        self.spawn_trash_bins()

        self.datacollector = DataCollector(
            model_reporters={
                "Littering": "total_trash",
            }
        )
        self.datacollector.collect(self)

    # description: places a number of persons on the field randomly
    # parameters: self.num_persons

    #Hier werden nach und nach alle Agenten auf dem Grid/Feld gespawnt
    # 1. die Personen personagents werden an random orten gespawnt 
    
    def spawn_persons(self):
        for i in range(self.num_persons):
            cell = self.random.choice(list(self.grid.coord_iter()))
            pos = cell[1:]
            new_person = PersonAgent(model=self, unique_id=self.next_id(), pos=pos,
                                     view_range=self.view_range, awareness=self.awareness, messiness=self.messiness)
            self.grid.place_agent(new_person,pos)
            self.schedule.add(new_person)
            
    # 2. Der Müll der zu Beginn rum liegt wird an random orten gespawnt 
    
    def spawn_trash(self):
        for i in range(self.num_trash):
            new_trash = TrashAgent(model=self,unique_id=self.next_id())
            cell = self.random.choice(list(self.grid.coord_iter()))
            pos = cell[1:]
            self.grid.place_agent(new_trash,pos)
            self.total_trash += 1

    # 3. Die Mülleimer werden an random orten gespawnt 
    
    def spawn_trash_bins(self):
        for i in range(self.num_trash_bins):
            cell = self.random.choice(list(self.grid.coord_iter()))
            pos = cell[1:]
            new_trash_bin = TrashBinAgent(model = self, unique_id = self.next_id(),
                                          capacity = self.trash_bin_capacity, pickup_interval=self.pickup_interval, pos = pos)
            self.grid.place_agent(new_trash_bin,pos)
            self.schedule.add(new_trash_bin) 
#isabelle: spawn_pub(self): for i in range(self.num_pub): cell = nicht random, pos = cell[3:4]        
    # Der einzelne Zeitschritt
    
    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

            
