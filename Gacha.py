from datetime import datetime
import time

import numpy as np
import genshinstats as gs
import gahca_calculation as gc

SSR_rate = 0.006
cpp = 2.2
cpr = 160

predicted = [36.7, 37.2, 36.4, 36.9, 36.6, 36.8]
predicted.sort(reverse=True)

class planer:

    # For start function!! Input
    start = None
    end = None
    current = 0

    budget = 0
    rate_up = 0
    roll_count = 0

    def __init__(self, uid: int, ltuid: int, ltoken: str, authURL: str):
        gs.set_cookie(account_id=ltuid, cookie_token=ltoken)
        gs.set_authkey(authURL)
        self.uid = uid

    def see_stat(self):
        return gs.get_user_stats(self.uid)['stats']

    def wished(self):
        hist = gs.get_wish_history(301)
        try:
            for i, d in enumerate(hist):
                if d['type'] == 'Character':
                    pass
        except:
            pass

    def free_possible(self):
        start = self.start.split('-')
        end = self.start.split('-')
        date_diff = (int(end[0]) - int(start[0])) * 365 + int((int(end[1]) - int(start[1])) * 30.41) + (int(end[2]) - int(start[2]))

        # Hoyo login
        for i in [7, 14, 21]:
            if int(start[2]) < i and int(end[2]) > i:
                self.current += 20
        
        # Daily quest
        self.current += date_diff * 60

        # Patch reward
        if start[2] == "1":
            self.current += 600

        # Patch live stream
        self.current += 300
        
        # From challange and event
        if int(start[2]) < 15:
            # Challange
            self.current += 1200
            # event
            self.current += 840
        else:
            # Challange
            self.current += 600
            # event
            self.current += 420

        print(f"Your Possible Crystals (without purchase) is {self.current} crystals")

    
    def perfect_timing(self, cheapest):
        crystal = int((self.budget*cheapest)/cpp)
        print(f"Total crystals gained from budget is {crystal} crystals")
        self.current += crystal
        print(f"Your Crystals {self.current} crystals")

        possible_pulls = int(self.current/cpr)
        print(f"Your possible pulls is {possible_pulls}")

        possible_pulls += self.roll_count

    def simulate(self):
        gc.prob_cal(0, self.rate_up, self.roll_count)