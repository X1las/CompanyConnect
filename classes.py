# Priority Logger for managing prints to terminal
class Logger:

    def __init__(self, muted: bool = False, priority: int = 1, suffix: str = "log"):
        self.muted = muted
        self.priority = priority
        self.suffix = suffix

    def log(self, message: str, priority: int = None):

        if priority:
            if priority <= self.priority:
                print(self.suffix + ": " + message)
        else:
            print(self.suffix + ": " + message)

# Source Class, Requires an id and logger


class Source:

    pairs = []

    def __init__(self, id, logObj: Logger, name=None, debth: int = None):
        self.id = id
        self.name = name
        self.debth = debth
        self.logger = logObj

    def search(self, target, data: dict = None, original=True):

        if not data:
            data = {}

        reached = False
        if target == self.id or target == self.name:
            reached = True

        if reached:
            if original:
                self.logger.log(
                    "source has found itself, and was not supposed to", priority=1)
                return
            else:
                data["tname"] = self.name
                return data

        if len(self.pairs) != 0:
            data[self.id] = True

            for i in self.pairs:
                result = i.search(target, data=data)
                if result:
                    if original:
                        self.logger.log("Found target with ownership of: " +
                                        str(result["upper"]*100) + result["tname"], priority=0)
                    else:
                        return result

# Pair Class, requires a to and from source, along with logger.
# Contains ownershit percentages as float whole numbers


class Pair:

    def __init__(self, fro: Source, to: Source, LogObj: Logger, average: float = None, real_up: float = None, real_down=None):
        self.fro = fro
        self.to = to
        self.average = average
        self.real_up = real_up
        self.real_down = real_down
        self.logger = LogObj

    def search(self, target, data: dict = None):

        if data and len(data) > 1:
            data = data
            data['upper'] *= (self.real_up/100)
            data['average'] *= (self.average/100)
            data['lower'] *= (self.real_down/100)
        else:
            data['upper'] = (self.real_up/100)
            data['average'] = (self.average/100)
            data['lower'] = (self.real_down/100)

        self.logger.log("found average: " + str(self.real_up), 3)

        try:
            if data[self.to.id]:
                return
        except:
            return self.to.search(target, data=data, original=False)
