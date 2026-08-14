from dataclasses import dataclass 
from datetime import time

@dataclass
class Agent:
    unique_id:str
    name:str
    routing_order:int
    start_time:time
    end_time:time
    on_vacation:bool
    active:bool
