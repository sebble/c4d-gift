#!/usr/bin/python
import os
import requests
import shutil
import pygame
import glob
from time import sleep
from subprocess import call

USER="sam"
DOMAIN="c4d.sbl.io"
TEMPDIR='audio-temp'
MUSICDIR='music'
running=True
audio_files=[]

def play_sound_fm( filename ):
    call(["./PiFmDma/PiFmDma", filename])
    return

def play_sound( filename ):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        sleep(0.2)
        continue

def play_sound_over( fn_bg=[], fn_fg=[] ):
    print(str(fn_fg))
    print(str(fn_bg))
    pygame.mixer.init()

    for m in fn_bg:
        pygame.mixer.music.load(m)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy() == True:
            for f in fn_fg:
                sleep(5)
                print("playing "+f)
                s=pygame.mixer.Sound(f)
                channel=s.play(0,0,200)
                while channel.get_busy() == True:
                    sleep(0.2)
                    continue
            
            # Finish immediately after audio if uncommented:
#            break


def mkdir_p( dirname ):
    if not os.path.exists( dirname ):
        os.makedirs( dirname )

def rm_r(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    elif os.path.exists(path):
        os.remove(path)


def main_test():
    files=glob.glob(TEMPDIR+"/*.wav")
    music=glob.glob(MUSICDIR+"/*.wav")
    play_sound_over(music, files)


def main():
    mkdir_p(TEMPDIR)
    music=glob.glob(MUSICDIR+"/*.wav")

    audio_files = requests.get("http://"+DOMAIN+"/server/list.php?user="+USER)
    files = audio_files.text.split("\n")
    files.pop()
    
    print("Files: "+ str(files))

    if len(files) == 0:
        print("No files to retrieve")
        exit()

    #retrieve
    for i,a in enumerate(files):
        audiopath = TEMPDIR +'/'+ a.split('/')[-1]
        files[i] = audiopath 
        r = requests.get("http://"+DOMAIN+"/server/"+a, stream=True)
        print("Retrieving file "+a)
        if r.status_code == 200:
            if not os.path.exists(audiopath):

                with open(audiopath, 'wb') as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
            else:    
                print("Already have file " + audiopath)
   
    #play
    play_sound_over( music,files ) 

#    rm_r(TEMPDIR)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting :)")
        running=False
        exit()

