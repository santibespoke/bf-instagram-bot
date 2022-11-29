import csv
import instaloader
from instaloader import Instaloader, Post, Profile
from pprint import pprint
import sys
import uuid


your_username = sys.argv[1] #The account that we are logged in, for example, bespoke_factory
target_profile = sys.argv[2] #The profile we are targeting, for example, bespoke_factory
target_lists = sys.argv[3] #Choose which user list we are targeting: following | followers | both

L = instaloader.Instaloader()
L.load_session_from_file(your_username)
P = Profile.from_username(L.context, target_profile)

target_count = ""

if (target_lists == "following"):
	print("Getting 'following...'")
	following = P.get_followees()
	newFollowing = sorted(following, key=lambda x: x.userid, reverse=False)
	target_count = str(following.count)

if (target_lists == "followers"):
	print("Getting 'followers...'")
	followers = P.get_followers()
	newFollowers = sorted(followers, key=lambda x: x.userid, reverse=False)
	target_count = str(followers.count)

if (target_lists == "both"):
	print("Getting both 'followers' and 'followings...'")
	following = P.get_followees()
	newFollowing = sorted(following, key=lambda x: x.userid, reverse=False)
	followers = P.get_followers()
	newFollowers = sorted(followers, key=lambda x: x.userid, reverse=False)
	target_count = str(following.count + followers.count)


print("Response from Instragram => " + target_profile + " (" + target_count + " users")

with open("./export/csvs/"+target_profile + "_" + target_count + "_" + target_lists + "_"+ str(uuid.uuid1())+".csv", 'w', newline='') as exportCSV:
	exportWriter = csv.writer(exportCSV, delimiter=',')
	exportWriter.writerow(['userid', 'username'])
	if 'newFollowing' in locals():
		print("Exporting followings")
		for f in newFollowing:
			pprint([f.userid, f.username])
			exportWriter.writerow([f.userid, f.username])
	if 'newFollowers' in locals():
		print("Exporting followers")
		for f in newFollowers:
			pprint([f.userid, f.username])
			exportWriter.writerow([f.userid, f.username])

print("Saved")
