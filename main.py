import psycopg2
import requests
import mimetypes
import os
from datetime import datetime
from pathlib import Path

# TODO: make it so this 1. uses a singular execute statement and 2. doesn't create duplicates
def pushToDB(file):
    #setup connection
    conn = psycopg2.connect(database="postgres", user = "postgres", password = "", host = "localhost", port = "5432")
    cursor = conn.cursor()
    #get file info
    fileType = mimetypes.guess_type(file)
    fileName = os.path.basename(file).replace("'", "")
    url = addToIpfs(file)
    #push file
    cursor.execute(f"""INSERT INTO filedata(filedir, filename, filetype, dateadded) VALUES('{url.replace("'", "")}', '{fileName}', '{fileType[0]}', {datetime.timestamp(datetime.now())}) ON CONFLICT DO NOTHING""")
    conn.commit()
    #get id assighned by db
    cursor.execute(f"""SELECT fileid FROM filedata WHERE filename = '{fileName}'""")
    workingId = cursor.fetchone()[0]
    source = 'bens laptop'
    #insert source
    cursor.execute(f"""INSERT INTO filesource(fileid, source) VALUES({workingId}, '{source}') ON CONFLICT DO NOTHING""")
    conn.commit()

    conn.close()
    return

def addToIpfs(filepath) -> str:
  # rb means open in binary. read binary
  with Path(filepath).open("rb") as fp:
      image_binary=fp.read()
      # we need to make post request to this endpoint.
      url = "http://127.0.0.1:5001/api/v0/add"
      # check the response object
      response = requests.post(url, files={"file": image_binary})
      ipfs_hash=response.json()["Hash"]
       # "./img/myImage.png" -> "myImage.png" split by "/" into array, take the last element 
      filename=filepath.split("/")[-1:][0]
      image_uri=f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
      return image_uri

def createTag(tagName):
    conn = psycopg2.connect(database="postgres", user = "postgres", password = "", host = "localhost", port = "5432")
    cursor = conn.cursor()
    cursor.execute(f"""INSERT INTO tags(tag) VALUES('{tagName}') ON CONFLICT DO NOTHING""")
    conn.commit()
    conn.close()
    return

#add mhedias
for a in os.listdir("A:/Desktop/vidya"):
    pushToDB("A:/Desktop/vidya/" + a)
# tags to organize, etc etc
for a in ['funny-hahas', 'pol', 'nikitas-home', 'kringe', 'slav', 'music-webm', 'ricardo', 'papes', 'spooky-stories', 'degeneratate-hahas', 
            'degenerate', 'cat', 'skeletalz', 'degenerate-informatiions', 'fotograph']:
    createTag(a)

#get by name
"SELECT filedir FROM filedata WHERE filename = '1.webm'"
#get by soource/ uploader
"SELECT filedir FROM filedata WHERE fileid IN (SELECT fileid FROM filesource WHERE source = 'bens laptop')"
#get by tags (aparently insert is slightly better optimised)
"""
SELECT filedir FROM filedata WHERE fileid in (
	SELECT fileid FROM filetag WHERE tagid in (
		SELECT tagid FROM tags WHERE tag IN ('funny-hahas', 'music-webm')))
"""
# get by 




# thing I need to make things go in tags
"INSERT INTO filetag(fileid, tagid) VALUES(5063, (SELECT tagid FROM tags WHERE tag = 'funny-hahas'))"