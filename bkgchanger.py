# Background changer © 2021 by Cleuton Sampaio is licensed under CC BY 4.0. 
# To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/
# Contains other people's ideas and code:
# - KNOWLEDGE DOCTOR (Chando Dhar) https://www.youtube.com/channel/UCwlhFburhQNOsfgeGOyRujg
# 
# Usage: 
# python bkgchanger.py -i <input video>.mp4 -o <output video>.mp4 -b <background image>.png
# - Video height and width must be the same of background image
# - Audio track is not copied. You need do use ffmpeg to extract original audio and merge to new video: 
#   -- Extract audio from original file: 
#      ffmpeg -i <original video>.mp4 -f mp3 -ab 192000 -vn <original audio>.mp3
#   -- Merge audio to generated video: 
#      ffmpeg -i <generated video>.mp4 -i <original audio>.mp3 -c copy -map 0:v:0 -map 1:a:0 <new video>.mp4
#
# This is still a work in progress
#
import cv2
import numpy as np
import argparse
import os
import random as rng

def nothing(x):
    pass

def find_hsv(video_file):
    l_green=None
    u_green=None
    mask=None
    pause=False
    video=cv2.VideoCapture(video_file)
    cv2.namedWindow('Trackbars')
    cv2.resizeWindow('Trackbars',300,300)
    cv2.createTrackbar('L-H', 'Trackbars', 0, 179, nothing)
    cv2.createTrackbar('L-S', 'Trackbars', 0, 255, nothing)
    cv2.createTrackbar('L-V', 'Trackbars', 0, 255, nothing)
    cv2.createTrackbar('U-H', 'Trackbars', 179, 179, nothing)
    cv2.createTrackbar('U-S', 'Trackbars', 255, 255, nothing)
    cv2.createTrackbar('U-V', 'Trackbars', 255, 255, nothing)
    frame_width = int(video.get(3))
    frame_height = int(video.get(4))
    pause=False

    while True: 
        if not pause:
            ret,frame=video.read()
        if ret==True:
            hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            l_h=cv2.getTrackbarPos('L-H', 'Trackbars')
            l_s=cv2.getTrackbarPos('L-S', 'Trackbars')
            l_v=cv2.getTrackbarPos('L-V', 'Trackbars')
            u_h=cv2.getTrackbarPos('U-H', 'Trackbars')
            u_s=cv2.getTrackbarPos('U-S', 'Trackbars')
            u_v=cv2.getTrackbarPos('U-V', 'Trackbars')
            l_green=np.array([l_h,l_s,l_v])
            u_green=np.array([u_h,u_s,u_v])
            mask=cv2.inRange(hsv,l_green,u_green)
            nmask = cv2.blur(mask, (10,10))
            res=cv2.bitwise_and(frame,frame,mask=mask)
            #removendo o background
            f=frame-res
            cv2.imshow("Frame (q-quit,w-retirar green,p-pausa/despausa)",frame)
            cv2.imshow("Mascara nmask",nmask)
            

            #contornos mascara
            #rcontours, hier_r = cv2.findContours(mask,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)

            #drawing = np.full((frame_height, frame_width, 3), 255, dtype=np.uint8)

            #for i in range(len(rcontours)):
            #    color = (0, 0, 0)
            #    cv2.drawContours(drawing, rcontours, i, color, 2, cv2.LINE_8, hier_r, 0)
            #r_areas = [cv2.contourArea(c) for c in rcontours]
            #max_rarea = np.max(r_areas)
            #for c in rcontours:
            #    print(f"cv2.contourArea(c) {cv2.contourArea(c)} max_rarea {max_rarea} max_rarea*0.7 {max_rarea*0.70}")
            #    if cv2.contourArea(c) < 100:
            #        cv2.drawContours(drawing,[c],-1,0,1)

            #cv2.imshow("Contornos",drawing)

            #kernel = np.ones((5,5),np.uint8)
            #erosion = cv2.erode(mask,kernel,iterations = 2)
            #nmask = cv2.blur(erosion, (10,10))
            #cv2.imshow("Contornos",erosion)
            
            res=cv2.bitwise_and(frame,frame,mask=nmask)
            f=frame-res
            cv2.imshow("Recorte novo",f)
            
            k=cv2.waitKey(1)
            if k==ord('q'):
                video.release()
                cv2.destroyAllWindows()
                quit()
            if k==ord('w'):
                #####
                mask = nmask
                #####
                video.release()
                cv2.destroyAllWindows()
                return ('w',frame_width,frame_height,l_green,u_green,mask)
            if k==ord('p'):
                pause=not pause
        else:
            video.release()
            cv2.destroyAllWindows()
            return ('w',frame_width,frame_height,l_green,u_green,mask)

def process_video(video_file,bkg_image,f_width,f_height,l_green,u_green,mask):
    video=cv2.VideoCapture(video_file)
    image=cv2.imread(bkg_image)
    size=(f_width,f_height)
    out = cv2.VideoWriter(video_output,cv2.VideoWriter_fourcc(*'MP4V'), 25, size)
    pause=False
    while True: 
        if not pause:
            ret,frame=video.read()
        if ret==True:
            hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            mask=cv2.inRange(hsv,l_green,u_green)
            res=cv2.bitwise_and(frame,frame,mask=mask)
            #removendo o background
            f=frame-res
            green_screen=np.where(f==0, image, f)
            cv2.imshow("Final (p: pausa/despausa)",green_screen)
            k=cv2.waitKey(1)
            if k==ord('p'):
                pause=not pause
            if pause==False:
                out.write(green_screen)
        else:
            out.release()
            video.release()
            cv2.destroyAllWindows()
            break

if __name__=="__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True,
        help="input video path")
    ap.add_argument("-b", "--background", required=True,
        help="input background image")
    ap.add_argument("-o", "--output", required=True,
        help="output video path")
    ap.add_argument("-d", "--dryrun", required=False,
        default="n",help="dry run (y/n)?")
    args = ap.parse_args()
    
    if not os.path.isfile(args.input):
        print("Input video file must exist")
        quit()
    video_file=args.input
    if os.path.isfile(args.output) and os.path.exists(args.output):
        print(f"Output file exists. Overwrite(y/n)")
        resp=input()
        if resp != "y":
            quit()
    video_output=args.output
    if not os.path.isfile(args.background):
        print(f"Background image must exist")
        quit()
    bkg_image=args.background
    dryrun=args.dryrun

    command,f_width,f_height,l_green,u_green,mask = find_hsv(video_file)


    if command=="w" and dryrun=="n":
        process_video(video_file,bkg_image,f_width,f_height,l_green,u_green,mask)

    print("Done!")
    print("To extract audio from original video: ")
    print("   ffmpeg -i <original input>.mp4 -f mp3 -ab 192000 -vn <audio name>.mp3")
    print("To merge audio with new video:")
    print("   ffmpeg -i <muted output>.mp4 -i <audio name>.mp3 -c copy -map 0:v:0 -map 1:a:0 <new output>.mp4")

