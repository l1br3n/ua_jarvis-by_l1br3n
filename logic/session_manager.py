import time

class SessionManager:
    def __init__(self):
        self.is_awake = False
        self.last_awake_time = 0
        self.timeout = 45  # Час активності Джарвіса
        
    def wake_up(self):
        self.is_awake = True
        self.last_awake_time = time.time()
        
    def check_sleep_state(self):
        if self.is_awake and (time.time() - self.last_awake_time > self.timeout):
            self.is_awake = False
            return True  
        return False