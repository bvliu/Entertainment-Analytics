import requests
import json
import urllib.request
import urllib.parse
import pymysql
import time
import datetime
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count
from urllib.parse import urlencode
import csv

appid = "1118759701501012"
appsecret = "0ad3fbde533a3e4662f36a86389e7764"
access_token="1118759701501012|x2pLWmhjDhSD3RbTG-qs_VyyNtE"

POOL = Pool(cpu_count()*2)

def generateQueryString(pageID):
	url = "https://graph.facebook.com/v2.7/%s/feed/?access_token=%s&fields=message,link,created_time,type,name,id,likes.limit(1).summary(true),comments.limit(1).summary(true),shares" % (pageID, access_token)
	return url

def scrapeFeedData(info):

	connection = pymysql.connect(host = '10.201.31.179', user = 'fooUser',
	password = 'pass', db = 'imdb', charset = 'utf8mb4',
	cursorclass = pymysql.cursors.DictCursor) 

	data = requestUntilSucceed(generateQueryString(info[1]))
	movieID = info[0]

	message = None
	link = None
	createdTime = None
	shares = None
	likes = None
	comments = None
	postID = None
	postType = None
	try:
		for post in data['data']:
			#print (post)
			if 'id' not in post:
				continue
			postID = post['id']
			print (postID)
			if 'type' in post:
				postType = post['type']
			if 'message' in post:
				message = post['message']
			if 'link' in post:
				link = post['link']
			if 'created_time' in post:
				createdTime = post['created_time']
				createdTime = createdTime[:10] + ' ' + createdTime[12:19]
				#print (createdTime)
			if 'shares' in post:
				shares = post['shares']['count']
			if 'likes' in post:
				likes = post['likes']['summary']['total_count']
			if 'comments' in post:
				comments = post['comments']['summary']['total_count']

			with connection.cursor() as cursor:
				sql = (
					"INSERT INTO `posts` (`id`, `fb_id`, `post_id`, `date`, `type`, `message`, `comments`, `likes`, `shares`, `link`) VALUES "
					"(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE `id`=%s, `fb_id`=%s, `date`=%s, `type`=%s, `message`=%s, `comments`=%s, `likes`=%s, `shares`=%s, `link`=%s"
					)
				cursor.execute(sql, (movieID, info[1], postID, createdTime, postType, message, comments, likes, shares, link, movieID, info[1], createdTime, postType, message, comments, likes, shares, link))


	except Exception as e:
		print (e)		


	connection.commit()
	connection.close()

def requestUntilSucceed(url):
	success = False
	tries = 0
	while success is False:
		print ('trying ' + str(tries) + " - " + url)
		tries+=1
		try:
			data = requests.get(url)
			if data.status_code == 200:
				success = True
			elif data.status_code == 500:
				print ('Internal Service error 500: ' + url)
				return
			elif 'error' in data.json():
				print ('Error ' + url)
				return
		except Exception as e:
			print (str(type(e)) + 'Error for URL %s: %s' % (url, datetime.datetime.now()))
			time.sleep(5)
	return data.json()

def getPages():
	queryList = []
	connection = pymysql.connect(host = 'localhost', user = 'root',
	password = 'pass', db = 'entertainment_analytics', charset = 'utf8mb4',
	cursorclass = pymysql.cursors.DictCursor) 

	with connection.cursor() as cursor:
		sql = "SELECT `id`, `fb_id` FROM `facebook` WHERE `fb_id` IS NOT NULL"
		cursor.execute(sql)
		for row in cursor:
			movieID = row['id']
			fbID = row['fb_id']
			queryList.append((movieID, fbID))

	connection.commit()
	connection.close()

	return queryList

if __name__ == '__main__':
	queryList = getPages()
	for x in queryList:
		print (x[0], x[1])
	POOL.map(scrapeFeedData, queryList)

