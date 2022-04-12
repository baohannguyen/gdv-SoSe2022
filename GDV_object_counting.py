import cv2
import numpy as np


def ChangeColor():
    # damit wird nur die maske erstellt
    lower_color = np.array([hue - hue_range, saturation -
                            saturation_range, value - value_range])
    upper_color = np.array([hue + hue_range, saturation +
                            saturation_range, value + value_range])
    # convert to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # create a mask
    mask = cv2.inRange(hsv, lower_color, upper_color)
    return mask


def load_Image(imgNumber):
    # wir haben insgesamt 6 Bilder, deswegen darf es nicht größer als 6 sein
    if imgNumber > 6:
        imgNumber = 6
    if imgNumber < 1:
        # darf nicht kleiner als 1 sein, weil sonst kein Bild angezeigt wird
        imgNumber = 1
    imgpath = 'images\\chewing_gum_balls0'+str(imgNumber)+'.JPG'
    # da wird der bildname mit der jeweiligen nummer eingespeichert
    img = cv2.imread(imgpath, cv2.IMREAD_COLOR)
    # If set, always convert image to the 3 channel BGR  color image
    # cv2.IMREAD_COLOR
    # img = cv2.resize(img, (800, 600))
    height = img.shape[0]
    width = img.shape[1]
    last_dim = img.shape[-1]
    return (img, height, width, last_dim)
    # Da werden die Bilder durchgegangen


class Farbe:
    def __init__(self, Name, Hue, Hue_range, Saturation, Saturation_Range, Value, Value_Range, Filter):
        self.Name = Name
        self.Hue = Hue
        self.Hue_Range = Hue_range
        self.Saturation = Saturation
        self.Saturation_Range = Saturation_Range
        self.Value = Value
        self.Value_Range = Value_Range
        self.Filter = Filter
    # die verschiedenen werte der farben
    # in eine klasse damit es ordentlicher aussieht


farbenArray = [
    Farbe('Blue', 100, 10, 150, 100, 255, 100, ['']),
    Farbe('Yellow', 27, 10, 155, 100, 255, 100, ['erosion', 'erosion']),
    Farbe('Red', 180, 10, 255, 94, 228, 101, ['dilatation', 'closing']),
    Farbe('Pink', 0, 10, 47, 100, 255, 40, ['erosion', 'dilatation', 'closing', 'erosion']),
    Farbe('White', 27, 10, 47, 100, 255, 20, ['opening']),
    Farbe('Green', 43, 10, 147, 100, 147, 100, ['erosion'])]
# die verschiedenen werte und filter der farben


hue = 100
hue_range = 10
saturation = 150
saturation_range = 100
value = 255
value_range = 100
# startwerte

imgNumber = 1
# Load the Image
(img, height, width, last_dim) = load_Image(imgNumber)

# create a mask
mask = ChangeColor()


def morph_shape(val):
    if val == 0:
        return cv2.MORPH_RECT
    elif val == 1:
        return cv2.MORPH_CROSS
    elif val == 2:
        return cv2.MORPH_ELLIPSE
# die verschiedenen Formen der morphologischen Methoden

# dilation with parameters
def dilatation(img, size, shape):
    element = cv2.getStructuringElement(shape, (2 * size + 1, 2 * size + 1), (size, size))
    return cv2.dilate(img, element)
    # gibt den radius an
    # +1 = wird nach unten verschoben, damit wir in der mitte sind
    # (size, size) = Mittelpunkt

# erosion with parameters
def erosion(img, size, shape):
    element = cv2.getStructuringElement(shape, (2 * size + 1, 2 * size + 1), (size, size))
    return cv2.erode(img, element)

# opening with parameters
def opening(img, size, shape):
    element = cv2.getStructuringElement(shape, (2 * size + 1, 2 * size + 1), (size, size))
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, element)

# closing with parameters
def closing(img, size, shape):
    element = cv2.getStructuringElement(shape, (2 * size + 1, 2 * size + 1), (size, size))
    return cv2.morphologyEx(img, cv2.MORPH_CLOSE, element)


kernel_size = 3
kernel_shape = morph_shape(0)
# zeigt dass wir das Quadrat für die morphologischen Methoden nehmen


masknames = ['original', 'opening', 'closing', 'dilatation', 'erosion'] 
# verschiedene Maskennamen (Methoden)
maskNamesList = []

red_BGR = (0, 0, 255)
green_BGR = (0, 255, 0)
blue_BGR = (255, 0, 0)
# Farben für den kreis und viereck erstellt
# Kreis und Viereck werden genutzt um die bälle zu finden
circle_size = 10
circle_thickness = 5
# Kreisgröße und dicke

min_size = 10
expected_roundness = 0.5

found = True
# dann kommt der satz das ein oder mehrere bälle gefunden wurde

colNumber = 0

while True:
    # sachen die wir nach oben übergeben

    imgcopy = img.copy()
    newmask = mask.copy()
    # maske und bild wird gekopiert

    for i in range(len(maskNamesList)):
        if maskNamesList[i] == 'opening':
            newmask = opening(newmask, kernel_size, kernel_shape)
            # wenn es opening ist wird in der konsole opening ausgedruckt
        if maskNamesList[i] == 'dilatation':
            newmask = dilatation(newmask, kernel_size, kernel_shape)
        if maskNamesList[i] == 'closing':
            newmask = closing(newmask, kernel_size, kernel_shape)
        if maskNamesList[i] == 'erosion':
            newmask = erosion(newmask, kernel_size, kernel_shape)

    connectivity = 8
    (numLabels, labels, stats, centroids) = cv2.connectedComponentsWithStats(newmask, connectivity, cv2.CV_32S)
    # centroids = punkte in der mitte, numlabels = anzahl der bälle (z.b bei gelb = 30)
    numRejected = 1
    for i in range(1, numLabels):
        # check size and roundness as plausibility
        topx = stats[i, cv2.CC_STAT_LEFT]
        topy = stats[i, cv2.CC_STAT_TOP]
        statWidth = stats[i, cv2.CC_STAT_WIDTH]
        statHeight = stats[i, cv2.CC_STAT_HEIGHT]
        # für die position der quadrate
        # x & y position und die größe & höhe davon

        if statWidth < min_size or statHeight < min_size:
            # min_size war oben (s. oben)
            # wenn breite & größe zu klein sind wereden sie weggeworfen
            # print('Found a too small component.')
            numRejected += 1
            # wird dann um 1 erhöht fall sie zu klein sind
            continue  # found component is too small to be correct
        if statWidth > statHeight:
            roundness = 1.0 / (statWidth/statHeight)
            # überprüft wie rund die bälle sind
            # welche rundung es hat -> expected roundness war 0.5
        elif statHeight > statWidth:
            roundness = 1.0 / (statHeight/statWidth)

# go through all (reasonable) found connected components
        if (roundness < expected_roundness):
            # wenn die rundung kleiner ist als die erwartene wird sie erhöht
            # damit sie zur bedingung passt
            # print('Found a component that is not round enough.')
            numRejected += 1
            # wenn es ein quadrat ist wird es weggeworfen
            continue  # ratio of width and height is not suitable


# find and draw center
        center = centroids[i]
        # zenterpunkt für den kreis
        center = np.round(center)
        center = center.astype(int)
        cv2.circle(imgcopy, center, circle_size, red_BGR, circle_thickness)
        # kreis wird gefunden und gezeichnet

# find and draw bounding box
        cv2.rectangle(imgcopy, (topx, topy), (topx + statWidth, topy + statHeight), blue_BGR, 3)
        # rechteck wird gefunden und gezeichnet

    if found:
        print('We have found ' + str(numLabels-numRejected) + ' '+farbenArray[colNumber].Name + ' balls.')
        found = False
# Satz wird gedruckt wenn alle bedingungen erfüllt sind
    cv2.imshow('Original image', imgcopy)
    cv2.imshow('Masked Image', newmask)

    key = cv2.waitKey(100)
    # 100 millisekunden
    if key == ord('q'):
        break

    if key == ord('t'):
        imgNumber = imgNumber+1
        (img, height, width, last_dim) = load_Image(imgNumber)
        mask = ChangeColor()
        found = True
        # damit kann man das bild ändern

    if key == ord('g'):
        imgNumber = imgNumber-1
        (img, height, width, last_dim) = load_Image(imgNumber)
        mask = ChangeColor()
        found = True

    if key == ord('e'):
        # damit kann ich die farbe wechseln
        colNumber = colNumber+1
        if(colNumber > 5):
            colNumber = 0
        found = True

        hue = farbenArray[colNumber].Hue
        hue_range = farbenArray[colNumber].Hue_Range
        saturation = farbenArray[colNumber].Saturation
        saturation_range = farbenArray[colNumber].Saturation_Range
        value = farbenArray[colNumber].Value
        value_range = farbenArray[colNumber].Value_Range
        maskNamesList = farbenArray[colNumber].Filter

        mask = ChangeColor()
        # variablen werden festgelegt

    if key == ord('n'):
        print('Hue: '+str(hue))
        print('Hue-Range : '+str(hue_range))
        print('Saturation : '+str(saturation))
        print('Saturation-Range : '+str(saturation_range))
        print('Value: '+str(value))
        print('Value-Range : '+str(value_range))
        print('Filter: '+str(maskNamesList))
        # farbwerte werden ausgedruckt

cv2.destroyAllWindows()
