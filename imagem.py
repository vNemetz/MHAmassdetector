import cv2 as cv
import os
import pandas as pan

dados = []
cap = cv.VideoCapture('nemetzedit.mp4')
fps = cap.get(cv.CAP_PROP_FPS)
t = 0

# deixa a imagem preta e branca, borra ela e depois binariza
def binariza (imagem):
    imagem = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)
    imagem = cv.GaussianBlur(imagem, (7,7), cv.BORDER_DEFAULT)
    binarizada = cv.threshold(imagem, 40, 255, cv.THRESH_BINARY_INV)[1]
    
    return binarizada
    

# enquanto o video estiver aberto, execute
while (cap.isOpened()):
    deucerto, frame = cap.read()
    
    # se o frame foi lido corretamente, 'deucerto' recebe True
    if not deucerto:
        print("Fim do vídeo")
        break
    if deucerto == True:
        cv.namedWindow("original", cv.WINDOW_NORMAL)
        cv.resizeWindow("original", 414, 736)
        cv.imshow("original", frame)
        # 'binariza' a imagem, coloca o que é mais claro com valor 255 e o que é mais escuro com valor 0
        binarizada = binariza(frame)

        # mostra a imagem binarizada
        cv.namedWindow("binarizada", cv.WINDOW_NORMAL)
        cv.resizeWindow("binarizada", 414, 736)
        cv.imshow("binarizada", binarizada)

        # encontra os contornos externos (borda) da massa
        borda = cv.findContours(binarizada, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]

        # inicia um loop que encontra, a partir da borda, coordenadas para um retângulo que contorna a massa
        for i in borda:
            area = cv.contourArea(i)
            if area > 600:
                #coordenadas do retângulo
                a,b,c,d = cv.boundingRect (i)
                
                # adiciona na matriz dados o instante de tempo e a posição do centro de massa em pixels
                dados.append({"t(s)":t, "posicao(m)": (((a + c)/2))})

                # incrementa o tempo levando em conta o tempo que se passa entre os frames da imagem
                t += 1/fps
                cv.rectangle(binarizada,(a,b),(a+c,b+d),(255,0,255),2)
                cv.imshow("binarizada", binarizada)
                centro_x=((a+c)/2)
                centro_y=((b+d)/2)
                print("Cx: ",centro_x,"Cy: ",centro_y)
        if cv.waitKey(25) & 0xFF == ord('q'): 
            break
    # termina o loop quando não houver mais frames
    else: 
        break

# joga os dados da matriz numa tabela
txt=pan.DataFrame(dados)
#cria um arquivo .csv com os dados da tabela
txt.to_csv("dados.csv", index=False)
# libera o vídeo e fecha as janelas
cap.release()
cv.destroyAllWindows()
os.system('python3 graph.py')
