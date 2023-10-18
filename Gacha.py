import genshinstats as gs
import gahca_calculation as gc

class planer:

    # For start function!! Input
    start = None
    end = None
    current = 0

    budget = 0
    rate_up = 0
    roll_count = -1

    def __init__(self, uid: int, ltuid: int, ltoken: str, authURL: str):
        gs.set_cookie(ltuid=ltuid, ltoken=ltoken)
        gs.set_authkey(authURL)
        self.uid = uid

    def see_stat(self):
        return gs.get_user_stats(self.uid)['stats']

    def wished(self):
        if self.roll_count == -1:
            self.roll_count = 0

        hist = None

        try:
            hist = gs.get_wish_history(301)
        except:
            return -1

        try:
            for d in hist:
                if d['type'] == 'Character' and d['rarity'] == 5:
                    break
                else:
                    self.roll_count += 1
        except:
            pass
        
        return self.roll_count
        
    def add_rolls(self, rolls):
        self.roll_count += rolls

    def free_possible(self, s, e, c: int):
        self.start, self.end, self.current = s, e, c
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

        return self.current

    def simulate(self):
        return gc.prob_cal(0, self.rate_up, self.roll_count)