from mundo import Mundo
from visao import Visao
from sonar import Sonar
from ia import IA
import sys

mundo = Mundo()

erro = False
if len(sys.argv) == 3:
    if sys.argv[1] == 'true':
        debub = True
    elif sys.argv[1] == 'false':
        debub = False
    else:
        erro = True
    try:
        largPixels = int(sys.argv[2])
    except:
        erro = True
if len(sys.argv) < 3 or erro == True:
    debub = False
    largPixels = 600

visao = Visao("calibr.wr", 0, largPixels, debub, mundo)
sonar = Sonar(2.0, mundo)

ia = IA(mundo)

'''
while True:
    visao.update()
    sonar.update()
    # print(mundo)  # For Debug
    ia.decisao()
'''

#visao.start()
#ia.start()

try:
    while True:
        visao.update()
        sonar.update()
        # print(mundo)  # For Debug
        ia.decisao()
except:
    visao.finaliza()
    ia.finalizar()
