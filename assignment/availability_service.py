from datetime import datetime

class AvailabilityService:
    
    def is_available(self, agent: str) -> bool:
        """
        Determin whether the agent is available for routing. 
        """
        availability = True
        now = datetime.now().time()
        if not(agent.start_time <= now <= agent.end_time):
            availability = False
        if agent.on_vacation == True:
            availability = False
        if agent.active == False:
            availability = False
        return availability


