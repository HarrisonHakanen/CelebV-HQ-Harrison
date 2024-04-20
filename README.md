Esse é um código alterado da base CelebV-HQ (https://celebv-hq.github.io/), que possui algumas partes além da extração da base CelebV-HQ propriamente dita.
O código desse resitório extrai a base CelebV-HQ em 4 threads diferentes e armazena os vídeos nas pastas downloaded_celebvhqPt1, downloaded_celebvhqPt2, downloaded_celebvhqPt3, downloaded_celebvhqPt4 
levando menos tempo para extração dos dados do código original. Além disso se caso precise desligar o computador ou por acaso alguma avaria ocorra, o processo irá continuar de onde parou,
evitando reprocessar todos os vídeos novamente.


Esse é o primeiro projeto para extração de faces, pois esse projeto os videos que muitas vezes são repetidos da mesma pessoa, o que pode ser ruim dependendo de que tipo 
de processamento irá ocorrer após a extração dos rostos.

Os projetos seguintes que devem serem executados para retirar melhores imagens são:
SeparaVideos.py (se encontra nesse mesmo repositório) - Esse código agrupa as faces do mesmo video por pastas.

ColetorDeFaces (https://github.com/HarrisonHakanen/ColetorDeFaces) - Esse código foi escrito em c++. Ele recorta 20 frames
(esse valor pode ser alterado conforme sua necessidade) e os armazena em pastas separadas.

RemoverFacesDuplicadas (https://github.com/HarrisonHakanen/RemovedorDeFacesDuplicadas) - Esse código foi escrito em c++. Muitas faces que vem originalmente do CelebV-HQ são na verdade a 
mesma pessoa porém em um momento diferente no video, isso da a impressão que você extraiu muitas pessoas quando na verdade não foram tantas pessoas, mas são as mesmas pessoas repetidas vezes.
Como o nome do projeto já sugere, ele pega os frames adquiridos no projeto anterior, compara com os frames das demais pessoas, caso já existir a pessoa em outro video, ele então concatena os frames.

Estou a disposição para auxílo caso precise.
