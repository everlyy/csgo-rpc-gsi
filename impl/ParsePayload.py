from .GameState import GameState

def parse_payload(gamestate, payload):
	if "round" in payload and "phase" in payload["round"]:
		gamestate.round_phase = payload["round"]["phase"]

	if "map" in payload:
		map_info = payload["map"]
		
		if "mode" in map_info:
			gamestate.map.mode = map_info["mode"]

		if "name" in map_info:
			gamestate.map.name = map_info["name"]

		if "phase" in map_info:
			gamestate.map.phase = map_info["phase"]

		if "round" in map_info:
			gamestate.map.round = map_info["round"]

		if "team_ct" in map_info:
			team = map_info["team_ct"]

			if "score" in team:
				gamestate.map.team_ct.score = team["score"]

			if "timeouts_remaining" in team:
				gamestate.map.team_ct.timeouts_remaining = team["timeouts_remaining"]

			if "matches_won_this_series" in team:
				gamestate.map.team_ct.matches_won_this_series = team["matches_won_this_series"]

		if "team_t" in map_info:
			team = map_info["team_t"]

			if "score" in team:
				gamestate.map.team_t.score = team["score"]

			if "timeouts_remaining" in team:
				gamestate.map.team_t.timeouts_remaining = team["timeouts_remaining"]

			if "matches_won_this_series" in team:
				gamestate.map.team_t.matches_won_this_series = team["matches_won_this_series"]

		if "num_matches_to_win_series" in map_info:
			gamestate.map.num_matches_to_win_series = map_info["num_matches_to_win_series"]

		if "current_spectators" in map_info:
			gamestate.map.current_spectators = map_info["current_spectators"]

		if "souvenirs_total" in map_info:
			gamestate.map.souvenirs_total = map_info["souvenirs_total"]

	if "player" in payload:
		player = payload["player"]

		if "steamid" in player:
			gamestate.player.steamid = player["steamid"]

		if "name" in player:
			gamestate.player.name = player["name"]

		if "observer_slot" in player:
			gamestate.player.observer_slot = player["observer_slot"]

		if "team" in player:
			gamestate.player.team = player["team"]

		if "activity" in player:
			gamestate.player.activity = player["activity"]

		if "state" in player:
			state = player["state"]

			if "health" in state:
				gamestate.player.state.health = state["health"]

			if "armor" in state:
				gamestate.player.state.armor = state["armor"]

			if "helmet" in state:
				gamestate.player.state.helmet = state["helmet"]

			if "flashed" in state:
				gamestate.player.state.flashed = state["flashed"]

			if "smoked" in state:
				gamestate.player.state.smoked = state["smoked"]

			if "burning" in state:
				gamestate.player.state.burning = state["burning"]

			if "money" in state:
				gamestate.player.state.money = state["money"]

			if "round_kills" in state:
				gamestate.player.state.round_kills = state["round_kills"]

			if "round_killhs" in state:
				gamestate.player.state.round_killhs = state["round_killhs"]

			if "equip_value" in state:
				gamestate.player.state.equip_value = state["equip_value"]

		if "weapons" in player:
			gamestate.player.weapons = player["weapons"]

		if "match_stats" in player:
			match_stats = player["match_stats"]

			if "kills" in match_stats:
				gamestate.player.match_stats.kills = match_stats["kills"]

			if "assists" in match_stats:
				gamestate.player.match_stats.assists = match_stats["assists"]

			if "deaths" in match_stats:
				gamestate.player.match_stats.deaths = match_stats["deaths"]

			if "mvps" in match_stats:
				gamestate.player.match_stats.mvps = match_stats["mvps"]

			if "score" in match_stats:
				gamestate.player.match_stats.score = match_stats["score"]