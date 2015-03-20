#!/usr/bin/python
import os
import requests
import pygame
from subprocess import call
from threading  import Thread

USER="sam"
DOMAIN="c4d.sbl.io"
TEMPDIR='audio-temp'
running=True
audio_files=[]

def play_sound_fm( filename ):
    call(["./PiFm/pifm", filename])
    return

def play_sound( filename ):
	pygame.mixer.init()
	pygame.mixer.music.load(filename)
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy() == True:
		continue

def mkdir_p( dirname ):
	if not os.path.exists( dirname ):
		os.makedirs( dirname )

def main():
	mkdir_p(TEMPDIR)

	audio_files = requests.get("http://"+DOMAIN+"/server/list.php?user="+USER)
	files = audio_files.text.split("\n")
	
	for a in files:
		audiopath=TEMPDIR +'/'+ a.split('/')[-1]
		
		r = requests.get("http://"+DOMAIN+"/server/"+a, stream=True)
		
		if r.status_code == 200:
			if os.path.exists(audiopath):
				print("Already have file " + audiopath)
				continue

			with open(audiopath, 'wb') as f:
				for chunk in r.iter_content(1024):
					f.write(chunk)
		
		print("Playing file "+ audiopath)
		play_sound( audiopath )
		#play_sound("./PiFm/sound.wav")


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("Exiting :)")
		running=False

