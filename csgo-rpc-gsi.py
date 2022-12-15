from config import *
from impl.GSIServer import GSIServer
from impl.DiscordRPC import DiscordRPC
import json

server = GSIServer(GSI_SERVER_ADDRESS, GSI_SERVER_TOKEN)
rpc = DiscordRPC.init_for_os(DISCORD_RPC_CLIENT_ID)

# List of map images that I've uploaded to the Discord application
# If a map is not on this list it'll fallback to a question mark image
map_images = [ "de_mirage", "cs_office", "de_cache", "de_nuke", "de_vertigo" ]

def set_rpc(gamestate):
	spectating = gamestate.player.steamid != YOUR_STEAMID
	player = f"{'spectating: ' if spectating else ''}{gamestate.player.name}"
	stats = f"{gamestate.player.match_stats.kills}/{gamestate.player.match_stats.assists}/{gamestate.player.match_stats.deaths}" if not spectating else ""

	# Make sure the team score of current player is in front
	team_scores = f"{gamestate.map.team_ct.score}:{gamestate.map.team_t.score}"
	if gamestate.player.team == "T":
		team_scores = f"{gamestate.map.team_t.score}:{gamestate.map.team_ct.score}"

	team_scores = f"[{team_scores}]"

	if gamestate.map.phase == "warmup":
		team_scores = "warmup"

	activity = {
		"assets": {
			"small_image": "csgo_logo",
			"small_text": "CS:GO",
		},
		"details": "In the main menu",
	}

	if gamestate.player.activity != "menu":
		activity["assets"]["large_image"] = gamestate.map.name if gamestate.map.name in map_images else "unknown_map"
		activity["assets"]["large_text"] = gamestate.map.name
		activity["details"] = f"{team_scores} {gamestate.map.mode} {gamestate.map.name}"
		activity["state"] = f"{player} {stats}"

	if SHOW_GITHUB_URL and (not HIDE_MY_PROFILE and not spectating):
		activity["buttons"] = []
		buttons = activity["buttons"]

		if SHOW_GITHUB_URL:
			activity["buttons"].append({
				"label": "GitHub",
				"url": "https://github.com/everlyy/csgo-rpc-gsi"
			})

		if not spectating and not HIDE_MY_PROFILE:
			activity["buttons"].append({
				"label": f"{gamestate.player.name}'s profile",
				"url": f"https://steamcommunity.com/profiles/{gamestate.player.steamid}"
			})

	rpc.set_activity(activity)

def on_payload(self, gamestate, payload):
	set_rpc(gamestate)

	with open("gamestate.json", "w") as file:
		file.write(json.dumps(payload, indent=4))

server.set_payload_callback(on_payload)
server.run()