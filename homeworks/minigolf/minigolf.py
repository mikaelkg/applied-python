class Player:
    def __init__(self, name):
        self._name = name
    @property
    def name(self):
        return self._name


class HitsMatch:
    def __init__(self, H, players):
        self._H = H
        self._players = players
        self._finished = False
        self._table = [tuple(player.name for player in self.players), *(tuple([None]*self.H) for player in self.players)]
        self._current_H = 1
        self._current_player = 0
        self._players_points = [{'points' : 0, 'hit' : False} for player in self.players]
    @property
    def H(self):
        return self._H
    @property
    def players(self):
        return self._players
    @property
    def finished(self):
        return self._finished
    @finished.setter
    def finished(self, value):
        self._finished = value
    def hit(self, success=False):
        if not self.finished:
            if success:
                self._players_points[self._current_player]['points'] += 1
                self._players_points[self._current_player]['hit'] = True
                self.update_table()
            else:
                self._players_points[self._current_player]['points'] += 1
                if self._players_points[self._current_player]['points'] == 9:
                    self._players_points[self._current_player]['points'] += 1
                    self._players_points[self._current_player]['hit'] = True
                    self.update_table()
            self._current_player = self.next_player()
        else:
            raise RuntimeError
    def get_table(self):
        return self._table
    def next_player(self):
        for i in range(1, len(self.players)+1):
            if not self._players_points[(self._current_player + i) % len(self.players)]['hit']:
                return (self._current_player + i) % len(self.players)

        self._players_points = [{'points' : 0, 'hit' : False} for player in self.players]
        self._current_H += 1
        if self._current_H == self.H + 1:
            self.finished = True
        return self._current_H - 1
    def update_table(self):
        buf = list(self._table[self._current_H])
        for i,player_point in enumerate(self._players_points):
            if player_point['hit']:
                buf[i] = player_point['points']
        self._table[self._current_H] = tuple(buf)
    def _get_column(self, x, y):
        return [x[i][y] for i in range(len(x))]
    def _extract_win(self,x,key):
        return min(x,key=key)
    def get_winners(self):
        if self.finished:
            transp_table = [self._get_column(self._table,i)[1:] for i in range(len(self._table[0]))]
            winners = []
            min_point = self._extract_win(transp_table, key = lambda x: sum(x))
            for i,j in enumerate(transp_table):
                if sum(j) == sum(min_point):
                    winners.append(self.players[i])

            return winners
        else:
            raise RuntimeError
class HolesMatch(HitsMatch):
    def __init__(self, H, players):
        super(HolesMatch, self).__init__(H, players)
        self.cycle = 0
        self.cycles = 1
    def hit(self, success=False):
        if not self.finished:
            if success:
                self._players_points[self._current_player]['hit'] = True
                self._players_points[self._current_player]['points'] = 1
                self.update_table()

            self._current_player = self.next_player()
        else:
            raise RuntimeError
    def any_win(self):
        for player in self._players_points:
            if player['hit']:
                return True
        return False
    def set_hit(self):
        for i,j in enumerate(self._players_points):
            self._players_points[i]['hit'] = True
    def next_player(self):
        self.cycle += 1 
        if (self.any_win() or self.cycles == 10) and (self.cycle == len(self.players)):
        
            self.set_hit()
            self.update_table()
  
            self._current_H += 1
            self._players_points = [{'points' : 0,'hit' : False} for player in self.players]
            self.cycle = 0
            self.cycles = 1
            if self._current_H == self.H + 1:
                self.finished = True
            return self._current_H - 1
        else:
            if self.cycle == len(self.players):
                self.cycle = 0
                self.cycles += 1
            return (self._current_player + 1) % len(self.players)
    def _extract_win(self,x,key):
        return max(x,key=key)
