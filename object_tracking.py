import cv2
import time
import math

# Coordenadas do ponto alvo
p1 = 530
p2 = 300

# Listas para rastrear as coordenadas do objeto
xs = []
ys = []

# Carregar o vídeo a partir do arquivo "bb3.mp4"
video = cv2.VideoCapture("bb3.mp4")

# Criar um rastreador KCF (Kernelized Correlation Filters)
tracker = cv2.TrackerKCF_create()

# Ler o primeiro quadro do vídeo
returned, img = video.read()

# Permitir que o usuário selecione a caixa delimitadora inicial na imagem
bbox = cv2.selectROI("Rastreando", img, False)

# Inicializar o rastreador com a imagem e a caixa delimitadora inicial
tracker.init(img, bbox)

# Imprimir a caixa delimitadora inicial
print(bbox)

# Função para desenhar a caixa delimitadora no quadro
def drawBox(img, bbox):
    x, y, w, h = int(bbox[0], bbox[1], bbox[2], bbox[3])

    # Desenhar a caixa delimitadora retangular
    cv2.rectangle(img, (x, y), ((x + w), (y + h)), (255, 0, 255), 3, 1)

    # Exibir o texto "Rastreando" acima da caixa delimitadora
    cv2.putText(img, "Rastreando", (75, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

# Função para rastrear o objeto e calcular a distância até o ponto alvo
def goal_track(img, bbox):
    
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    # Obter os pontos centrais da caixa delimitadora
    c1 = x + int(w/2)
    c2 = y + int(h/2)

    # Desenhar um pequeno círculo nos pontos centrais
    cv2.circle(img, (c1, c2), 2, (0, 0, 255), 5)

    # Desenhar um círculo verde no ponto alvo
    cv2.circle(img, (int(p1), int(p2)), 2, (0, 255, 0), 3)

    # Calcular a distância entre os pontos centrais e o ponto alvo
    dist = math.sqrt(((c1 - p1)**2)+ (c2 - p2)**2)
    print(dist)


    # Se a distância for menor ou igual a 20 pixels, exibir "Cesta"
    if(dist <= 20):
        cv2.putText(img, "Cesta", (300,90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0))


    # Adicionar as coordenadas dos pontos centrais às listas xs e ys
    xs.append(c1)
    ys.append(c2)

    # Desenhar círculos nos pontos centrais anteriores
    for i in range(len(xs) - 1):
        cv2.circle(img, (xs[i], ys[i]), 2, (0, 0, 255), 5)

# Loop principal para processar o vídeo
while True:
    # Ler o próximo quadro do vídeo
    check, img = video.read()   

    # Atualizar o rastreador com a imagem atual e a caixa delimitadora
    success, bbox = tracker.update(img)

    # Chamar a função drawBox() para desenhar a caixa delimitadora
    if success:
        drawBox(img, bbox)
    else:
        # Se o rastreamento falhar, exibir "Errou"
        cv2.putText(img, "Errou", (75,90), cv2.FONT_HERSHEY_SIMPLEX, 0.7(0,0,255))

    # Chamar a função goal_track() para rastrear o objeto e o ponto alvo
    goal_track(img, bbox)

    # Exibir o vídeo resultante
    cv2.imshow("resultado", img)

    # Sair do loop quando a barra de espaço for pressionada
    key = cv2.waitKey(25)
    if key == 32:
        print("Interrompido")
        break

# Liberar o recurso de vídeo e fechar a janela
video.release()
cv2.destroyAllWindows()


# Sorria