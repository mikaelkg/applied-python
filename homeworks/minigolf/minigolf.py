from abc import ABCMeta, abstractmethod
class Player:
    def __init__(self, name):
        self._name = name
    @property
    def name(self):
        return self._name
class Match(metaclass=ABCMeta):
    HITS_LIMIT = 10
    def __init__(self, h, players):
        self._h = h
        self._players = players
        self._finished = False
        self._table = [tuple(player.name for player in self.players), *(tuple([None]*self.h) for player in self.players)]
        self._current_h = 1
        self._current_player = 0
        self._players_points = [{'points' : 0, 'hit' : False} for player in self.players]
    @property
    def h(self):
        return self._h
    @property
    def players(self):
        return self._players
    @property
    def finished(self):
        return self._finished
    @finished.setter
    def finished(self, value):
        self._finished = value
    def get_table(self):
        return self._table
    def _update_table(self):
        buf = list(self._table[self._current_h])
        for i,player_point in enumerate(self._players_points):
            if player_point['hit']:
                buf[i] = player_point['points']
        self._table[self._current_h] = tuple(buf)
    def _get_column(self, x, y):
        return [x[i][y] for i in range(len(x))]

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
    @abstractmethod
    def hit(self, success=False):
        pass
    @abstractmethod
    def _next_player(self):
        pass
    @abstractmethod
    def _extract_win(self,x,key):
        pass
class HitsMatch(Match):

    def hit(self, success=False):
        if not self.finished:
            if success:
                self._players_points[self._current_player]['points'] += 1
                self._players_points[self._current_player]['hit'] = True
                self._update_table()
            else:
                self._players_points[self._current_player]['points'] += 1
                if self._players_points[self._current_player]['points'] == Match.HITS_LIMIT - 1:
                    self._players_points[self._current_player]['points'] += 1
                    self._players_points[self._current_player]['hit'] = True
                    self._update_table()
            self._current_player = self._next_player()
        else:
            raise RuntimeError

    def _next_player(self):
        for i in range(1, len(self.players)+1):
            if not self._players_points[(self._current_player + i) % len(self.players)]['hit']:
                return (self._current_player + i) % len(self.players)

        self._players_points = [{'points' : 0, 'hit' : False} for player in self.players]
        self._current_h += 1
        if self._current_h == self.h + 1:
            self.finished = True
        return self._current_h - 1
    def _extract_win(self,x,key):
        return min(x,key=key)


class HolesMatch(Match):
    def __init__(self, h, players):
        super(HolesMatch, self).__init__(h, players)
        self.cycle = 0
        self.cycles = 1
    def hit(self, success=False):
        if not self.finished:
            if success:
                self._players_points[self._current_player]['hit'] = True
                self._players_points[self._current_player]['points'] = 1
                self._update_table()

            self._current_player = self._next_player()
        else:
            raise RuntimeError
    def _any_win(self):
        for player in self._players_points:
            if player['hit']:
                return True
        return False
    def _set_hit(self):
        for i,j in enumerate(self._players_points):
            self._players_points[i]['hit'] = True
    def _next_player(self):
        self.cycle += 1 
        if (self._any_win() or self.cycles == Match.HITS_LIMIT) and (self.cycle == len(self.players)):
        
            self._set_hit()
            self._update_table()
  
            self._current_h += 1
            self._players_points = [{'points' : 0,'hit' : False} for player in self.players]
            self.cycle = 0
            self.cycles = 1
            if self._current_h == self.h + 1:
                self.finished = True
            return self._current_h - 1
        else:
            if self.cycle == len(self.players):
                self.cycle = 0
                self.cycles += 1
            return (self._current_player + 1) % len(self.players)
    def _extract_win(self,x,key):
        return max(x,key=key)
