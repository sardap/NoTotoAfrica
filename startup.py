import argparse
import requests
import json
import editdistance
import random

# array incase more pop up
TOTO_AFRICAS = [
	"2374M0fQpWi3dLnB54qaLX"
]

def get_header(access_token):
	return {
		'Content-Type': "application/json",
		'Authorization': "Bearer {}".format(access_token),
		'Connection': "keep-alive",
		'cache-control': "no-cache"
	}

def reverse_tracks(tracks):
	return tracks[::-1]

def remove_toto_africa_from_playlist(access_token="", playlist_id=-1):
	print("Removing toto africa from {}".format(playlist_id))
	url = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)

	request_ary = []
	for i in TOTO_AFRICAS:
		request_ary.append({ "uri" : "spotify:track:{}".format(i) })

	request_playload_json = { "tracks" : request_ary }
	
	payload = json.dumps(request_playload_json)
	headers = get_header(access_token)

	response = requests.request("DELETE", url, data=payload, headers=headers)

	return response.status_code == 200

def get_playlists(access_token=""):
	print("Getting playlists")
	url = "https://api.spotify.com/v1/me/playlists"

	headers = get_header(access_token)

	response = requests.request("GET", url, headers=headers)
	
	result = []

	if response.status_code != 200:
		print("failled to get playlist by name retrying")
		return get_playlists(access_token)
	else:
		for i in json.loads(response.text)["items"]:
			result.append(i["id"])
	
	return result

def parse_arguments():
	parser = argparse.ArgumentParser(description='Sort a Spotify playlist by a feature')
	parser.add_argument('access_token', type=str, help='access token for Spotify')
	return parser.parse_args()

def main():
	args = parse_arguments()

	playlist_ids = get_playlists(
		access_token=args.access_token
	)

	for playlist_id in playlist_ids:
		remove_toto_africa_from_playlist(
			access_token=args.access_token,
			playlist_id=playlist_id
		)


main()