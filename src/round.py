class Round:
    def __init__(self, guess, target):
        self.guess = guess
        self.target = target

    
    def compare_name(self):
        if self.guess.name == self.target.name:
            return self.target.name
        else : 
            return "X"
        
    def compare_age(self):
        if self.guess.age == self.target.age:
            return self.target.age
        elif self.guess.age > self.target.age:
            return "target is younger"
        elif self.guess.age < self.target.age:
            return "target is older"
        else:
            return None
    def compare_nation(self):
        if self.guess.nationality == self.target.nationality:
            return self.target.nationality
        else :
            return "X"
    def compare_club(self):
        if self.guess.club == self.target.club:
            return self.target.club
        else:
            return "X"
    def compare_position(self):
        if self.guess.position == self.target.position:
            return self.target.position
        elif self.decide_position_group(self.guess.position) == self.decide_position_group(self.target.position):
            return self.decide_position_group(self.target.position)
        else :
            return "X"
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
            return self.target.number
        elif self.guess.number > self.target.number:
            return "target player's number is lower"
        elif self.guess.number < self.target.number:
            return "target player's number is higher"
    def evaluate(self): 
        return {
            "name": self.compare_name(),
            "age": self.compare_age(),
            "nationality": self.compare_nation(),
            "club": self.compare_club(),
            "position": self.compare_position(),
            "number": self.compare_number()
        }

