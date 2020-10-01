import dgdl
import re
import ast

class Protocol:
    """
    Class to manage protocols, including creating, updating and testing
    """
    ERROR="error"
    OK="ok"

    def __init__(self, dgdl):

        self.dgdl = dgdl

        if self.dgdl is None:
            raise ValueError("DGDL is required")

        # regexes
        self.player_regex = re.compile(r"player\(([^\(\)]+)\)")
        self.player_spec_regex = re.compile(r"([^:{}, ]+):(?:([^:,{} ]+)|{([^{}]+)})")
        self.description_regex = re.compile(r"\/\*[\s]+description:[\s]+(.*)[\s]+\*\/",re.IGNORECASE)

    def test(self):
        """
        Test this protocol for syntax errors etc.
        """
        game = dgdl.DGDLParser().parse(input=self.dgdl)

        if isinstance(game, list):
            return game, Protocol.ERROR
        else:
            return ast.literal_eval(game.__repr__()), Protocol.OK

    def get_players(self):
        """
        Get the players for this protocol
        """
        matches = re.findall(self.player_regex, self.dgdl)
        players = []

        for m in matches:
            if m.strip() != "":
                player = {}
                for p in re.findall(self.player_spec_regex, m.strip()):
                    p = [x for x in p if x.strip() != ""]
                    if p[0] == "roles":
                        player[p[0]] = [r.strip() for r in p[1].split(",")]
                    else:
                        player[p[0]] = p[1]
                players.append(player)
        return players

    def get_description(self):
        """
        Gets the description of this protocol based on the "description" keyword
        """
        matches = re.findall(self.description_regex, self.dgdl)

        for m in matches:
            m = m.strip()
            if m != "":
                return m

        return ""
