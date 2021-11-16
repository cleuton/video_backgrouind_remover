# Background video changer
## Livre-se da tela verde!

![](./logo_preto_fundo_branco.png)

Aproveite e conheça os meus cursos na [**Udemy**](https://www.udemy.com/user/cleutonsampaio/):

[![](./cursos.jpeg)](https://www.udemy.com/user/cleutonsampaio/)

[**PORTUGUESE VERSION**](./portuguese.md)

O efeito "chroma key" é muito difícil de conseguir com as ferramentas gratuitas ou open source. 

Como produtor de conteúdo em vídeo, eu já tentei várias ferramentas. As melhores são as baseadas em Inteligência artificial, mas são muito caras exigindo pagamentos mensais. 

Nem mesmo ferramentas como o Openshot conseguem fazer este efeito de maneira satisfatória. 

Então, encontrei um trabalho de [**Chando Dhar**](https://www.youtube.com/channel/UCwlhFburhQNOsfgeGOyRujg) que me motivou a escrever esta ferramenta simples. Dá para melhorar muito, mas, por enquanto, é o que estou utilizando. 

## Uso: 
python bkgchanger.py -i "inputvideo".mp4 -o "output video".mp4 -b "background image".png
- A altura e largura do vídeo deve ser a mesma da imagem de fundo;
- A trilha de áudio não é copiada, mas você pode extrair do vídeo original com ffmpeg: 
   -- Extrair áudio do vídeo original: 
      ffmpeg -i "original video".mp4 -f mp3 -ab 192000 -vn "original audio".mp3
   -- Inserir o áudio original no novo vídeo: 
      ffmpeg -i "generated video".mp4 -i "original audio".mp3 -c copy -map 0:v:0 -map 1:a:0 "new video".mp4

Este ainda é um trabalho em progresso.