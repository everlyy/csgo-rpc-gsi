class PlayerState:
	def __init__(self):
		self.health = 0
		self.armor = 0
		self.helmet = False
		self.flashed = 0
		self.smoked = 0
		self.burning = 0
		self.money = 0
		self.round_kills = 0
		self.round_killshs = 0
		self.equip_value = 0

class PlayerMatchStats:
	def __init__(self):
		self.kills = 0
		self.assists = 0
		self.deaths = 0
		self.mvps = 0
		self.score = 0

class Player:
	def __init__(self):
		self.steamid = ""
		self.name = ""
		self.observer_slot = -1
		self.team = ""
		self.activity = ""
		self.state = PlayerState()
		self.weapons = {}
		self.match_stats = PlayerMatchStats()

class Map:
	def __init__(self):
		self.mode = ""
		self.name = ""
		self.phase = ""
		self.round = 0
		self.team_ct = Team()
		self.team_t = Team()
		self.num_matches_to_win_series = 0
		self.current_spectators = 0
		self.sourvenirs_total = 0

class Team:
	def __init__(self):
		self.score = 0
		self.timeouts_remaining = 0
		self.matches_won_this_series = 0

class GameState:
	def __init__(self):
		self.map = Map()
		self.player = Player()
		self.round_phase = ""