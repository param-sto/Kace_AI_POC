from datetime import datetime

class AvailabilityService:
    def is_availible(self, agent):
        """
        Determin 
        """
    def is_on_shift(self, agent:str) -> bool:
        """
        Determine wheter the agent is on shift.
        """
        now = datetime.now().time()
        if agent.shift_start <= now <= agent.shift_end:
            return True
        return False

    #def is_on_vacation(self, agent):

