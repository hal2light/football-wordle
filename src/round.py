class Round:
    def __init__(self, guess, target):
        self.guess = guess
        self.target = target

    
    def compare_name(self):
        if self.guess.name == self.target.name:
            return {"value":self.guess.name, "status": "correct"}
        else : 
            return {"value":self.guess.name, "status": "wrong"}

        
    def compare_age(self):
        if self.guess.age == self.target.age:
            return {"value": self.guess.age, "status": "correct"}
        elif self.guess.age > self.target.age:
            return {"value":self.guess.age, "status": "lower"}
        elif self.guess.age < self.target.age:
            return {"value":self.guess.age, "status": "higher"}
        else:
            return None
    def compare_nation(self):
        if self.guess.nationality == self.target.nationality:
            return {"value":self.guess.nationality, "status": "correct"}

        else :
            return {"value":self.guess.nationality, "status": "wrong"}

    def compare_club(self):
        if self.guess.club == self.target.club:
            return {"value":self.guess.club, "status": "correct"}
        else:
            return {"value":self.guess.club, "status": "wrong"} 
    def compare_position(self):
        if self.guess.position == self.target.position:
            return {"value":self.guess.position, "status": "correct"}
        elif self.decide_position_group(self.guess.position) == self.decide_position_group(self.target.position):
            return {"value":self.decide_position_group(self.guess.position), "status": "group_match"}
        else :
            return {"value":self.guess.position, "status": "wrong"}
    def decide_position_group(self, position):
        match position:
            case "GK":
                return "GK"
            case "CB" | "LB" | "RB" |"LWB" | "RWB" :
                return "DEF"
            case "CDM" | "CM" | "CAM" | "LM" | "RM" :
                return "MID"
            case "ST" | "CF" | "LW" | "RW" | "SS":
                return "FWD"
            case _:
                return None
    def compare_number(self):
        if self.guess.number == self.target.number:
            return {"value":self.guess.number, "status": "correct"}
        elif self.guess.number > self.target.number:
            return {"value":self.guess.number, "status": "lower"}
        elif self.guess.number < self.target.number:
            return {"value":self.guess.number, "status": "higher"}
    def evaluate(self): 
        return {
            "name": self.compare_name(),
            "age": self.compare_age(),
            "nationality": self.compare_nation(),
            "club": self.compare_club(),
            "position": self.compare_position(),
            "number": self.compare_number()
        }

