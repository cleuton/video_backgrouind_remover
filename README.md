# Background video changer
## Get rid of the green screen

![](./logo_preto_fundo_branco.png)

Aproveite e conheça os meus cursos na [**Udemy**](https://www.udemy.com/user/cleutonsampaio/):

[![](./cursos.jpeg)](https://www.udemy.com/user/cleutonsampaio/)

[**PORTUGUESE VERSION**](./portuguese.md)

The "**chroma key**" effect is very difficult to achieve with free or open source tools.

As a video content producer, I've tried several tools. The best ones are based on artificial intelligence, but they are very expensive and require monthly payments.

Not even tools like Openshot can do this effect satisfactorily.

Then I found a work by [**Chando Dhar**](https://www.youtube.com/channel/UCwlhFburhQNOsfgeGOyRujg) that motivated me to write this simple tool. You can improve a lot, but for now, that's what I'm using.

## Usage: 
python bkgchanger.py -i "inputvideo".mp4 -o "output video".mp4 -b "background image".png
- Video height and width must be the same of background image
- Audio track is not copied. You need do use ffmpeg to extract original audio and merge to new video: 
   -- Extract audio from original file: 
      ffmpeg -i "original video".mp4 -f mp3 -ab 192000 -vn "original audio".mp3
   -- Merge audio to generated video: 
      ffmpeg -i "generated video".mp4 -i "original audio".mp3 -c copy -map 0:v:0 -map 1:a:0 "new video".mp4

This is still a work in progress