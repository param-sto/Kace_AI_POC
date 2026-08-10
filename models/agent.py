from dataclasses import dataclass 
from datetime import time

@dataclass
class Agent:
    id:str
    name:str
    email:str

    routing_order:int

    shift_start:time
    shift_end:time

    on_vacation:bool
    active:bool

    active_tickets:int
