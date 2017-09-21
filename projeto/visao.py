from threading import Thread
import imutils
import cv2
import pickle

class Visao(Thread):
    '''Responsavel pelo tratamento da imagem vinda da camera'''

    def __init__(self, arquivo, numCam, largPixels, debug, mundo):
        # type: (object, int, int, bool, Mundo) -> None
        """
Inicializa o objeto Visao
        :param arquivo: Arquivo com os limites das cores
        :param numCam: Numero da camera usada
        :param largPixels: Largura da imgem em pixels
        :param debug: Caso True mostra a imagem para debug
        :param mundo: Objeto mundo
        """

        '''
        self.colorsLimits = {'blue': [(101, 125, 81), (120, 255, 255)],
                             'green': [(32, 57, 106), (68, 216, 215)],
                             'red': [[(0, 111, 113), (7, 244, 189)], [(179, 229, 156), (179, 229, 156)]]}
        '''

        with open('../calibr.wr', 'rb') as input:
            self.colorsLimits = pickle.load(input)
        
        print(self.colorsLimits)

        self.camera = cv2.VideoCapture(numCam)
        self.largPixels = largPixels
        self.debug = debug

        self.mundo = mundo

        self.mundo.montaListaBexiga(self.colorsLimits.keys())

        Thread.__init__(self)

    def update(self):
        """
Atualiza as informacoes do Mundo a partir da imagem da camera
        """
        (grabbed, frame) = self.camera.read()

        frame = imutils.resize(frame, width=self.largPixels)  # 600px -> menos px, mais rapido de processar

        frameHeight = len(frame)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #hsv = frame

        for color, colorLim in self.colorsLimits.iteritems():
            # Criacao e tratamendo da mascara
            if color == 'red':
                mask1 = cv2.inRange(hsv, colorLim[0][0], colorLim[0][1])
                mask1 = cv2.erode(mask1, None, iterations=2)
                mask1 = cv2.dilate(mask1, None, iterations=2)
                mask2 = cv2.inRange(hsv, colorLim[1][0], colorLim[1][1])
                mask2 = cv2.erode(mask2, None, iterations=2)
                mask2 = cv2.dilate(mask2, None, iterations=2)
                mask = mask2+mask1
            else:
                mask = cv2.inRange(hsv, colorLim[0], colorLim[1])
                mask = cv2.erode(mask, None, iterations=2)
                mask = cv2.dilate(mask, None, iterations=2)

            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)[-2]
            center = None

            detect = False

            if len(cnts) > 0:
                c = max(cnts, key=cv2.contourArea)
                approx = cv2.approxPolyDP(c, 0.01 * cv2.arcLength(c, True), True)
                area = cv2.contourArea(c)
                (x, y, w, h) = cv2.boundingRect(approx)

                #((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                if h > 10:
                    #cv2.circle(frame, center, 5, (0, 0, 255), -1)
                    #cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                    x = (center[0]-(self.largPixels/2.0))/float((self.largPixels/2.0))
                    y = (center[1] - (frameHeight/ 2.0)) / float((frameHeight/2.0))
                    h = h/float(frameHeight)

                    self.mundo.setBexiga(color, x, y, h, area)
                    self.mundo.temBexiga = True
                    detect = True
                if self.debug:
                    cv2.drawContours(frame, c, -1, (255, 0, 0), 3)

            if detect == False:
                self.mundo.bexigaInvisivel(color)

        if self.debug:
            frame = cv2.flip(frame, 1)
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF

    def run(self):
        """
Metodo a rodar na Thread
        """
        while True:
            self.update()

    def finaliza(self):
        """
Libera a camera e destroi as janelas. Chamar ao final do programa.
        """
        self.camera.release()
        cv2.destroyAllWindows()