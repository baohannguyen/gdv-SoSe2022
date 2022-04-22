import cv2
import numpy as np
import glob


def change_Color():
    # function that adjust the color mask
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
    # function that reads the image and returns it+its parameters
    # wir haben insgesamt 6 Bilder, deswegen darf es nicht größer als 6 sein
    if imgNumber > len(images):
        imgNumber = 1
    if imgNumber < 1:
        # darf nicht kleiner als 1 sein, weil sonst kein Bild angezeigt wird
        imgNumber = len(images)
    print(imgNumber)
    # da wird der bildname mit der jeweiligen nummer eingespeichert
    img = images[imgNumber-1]
    # If set, always convert image to the 3 channel BGR  color image
    # cv2.IMREAD_COLOR
    # img = cv2.resize(img, (800, 600))
    height = img.shape[0]
    width = img.shape[1]
    last_dim = img.shape[-1]
    return (img, height, width, last_dim, imgNumber)
    # Da werden die Bilder durchgegangen


class Color:
    def __init__(self, Name, Hue, Hue_range, Saturation, Saturation_Range, Value, Value_Range, Shape, Roundness, Filter):
        self.Name = Name
        self.Hue = Hue
        self.Hue_Range = Hue_range
        self.Saturation = Saturation
        self.Saturation_Range = Saturation_Range
        self.Value = Value
        self.Value_Range = Value_Range
        self.Shape = Shape
        self.Roundness = Roundness
        self.Filter = Filter
    # die verschiedenen werte der farben
    # in eine klasse damit es ordentlicher aussieht


colorArray = [
    Color('Blue', 100, 10, 160, 100, 255, 100, 2, 0.5, ['erosion']),
    Color('Yellow', 27, 10, 155, 100, 255, 100, 0, 0.2, ['erosion', 'erosion', 'erosion', 'dilation']),
    Color('Red', 180, 10, 255, 94, 228, 101, 2, 0.5, ['dilatation', 'closing']),
    Color('Pink', 0, 10, 47, 100, 255, 40, 2, 0.5, ['erosion', 'dilatation', 'closing', 'erosion']),
    Color('White', 27, 10, 47, 100, 255, 20, 2, 0.5, ['opening']),
    Color('Green', 43, 10, 147, 100, 147, 100, 2, 0.5, ['erosion']),
    Color('Red-Alt', 165, 10, 205, 100, 155, 100, 2, 0.5, ['']),
    Color('Pink-Alt', 170, 10, 30, 40, 255, 40, 2, 0.5, ['']),
    Color('White-alt', 0, 1, 0, 1, 255, 3, 0, 0.5, ['dilation', 'dilation', 'erosion', 'erosion', 'erosion', 'erosion', 'erosion', 'dilation', 'dilation',
         'dilation'])]
# die verschiedenen werte und filter der farben

# get starting values
collorNumber = 0

hue = colorArray[collorNumber].Hue
hue_range = colorArray[collorNumber].Hue_Range
saturation = colorArray[collorNumber].Saturation
saturation_range = colorArray[collorNumber].Saturation_Range
value = colorArray[collorNumber].Value
value_range = colorArray[collorNumber].Value_Range
filterList = colorArray[collorNumber].Filter
shape = colorArray[collorNumber].Shape
expected_roundness = colorArray[collorNumber].Roundness
#startwerte

# get all images
images = [cv2.imread(file, cv2.IMREAD_COLOR) for file in glob.glob('images\\chewing_gum_balls**.jpg')]

imgNumber = 1
# Load the first Image
(img, height, width, last_dim, imgNumber) = load_Image(imgNumber)

# create the first mask
mask = change_Color()


def morph_shape(val):
    if val == 0:
        return cv2.MORPH_RECT
    elif val == 1:
        return cv2.MORPH_CROSS
    elif val == 2:
        return cv2.MORPH_ELLIPSE
# die verschiedenen Formen der morphologischen Methoden

kernel_size = 3
kernel_shape = morph_shape(shape)
# zeigt dass wir das Quadrat für die morphologischen Methoden nehmen


# dilation with parameters
def dilation(img, size, shape):
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


# kernel_size = 3
# kernel_shape = morph_shape(0)




# masknames = ['original', 'opening', 'closing', 'dilatation', 'erosion'] 
# verschiedene Maskennamen (Methoden)
# maskNamesList = []

red_BGR = (0, 0, 255)
green_BGR = (0, 255, 0)
blue_BGR = (255, 0, 0)
# Farben für den kreis und viereck erstellt
# Kreis und Viereck werden genutzt um die bälle zu finden
circle_size = 6
circle_thickness = 3
# Kreisgröße und dicke

min_size = 10
# expected_roundness = 0.5

found = True
# dann kommt der satz das ein oder mehrere bälle gefunden wurde


while True:
    # sachen die wir nach oben übergeben

    imgcopy = img.copy()
    newmask = mask.copy()
    # maske und bild wird gekopiert
    # goes through the filterlist and morphs the mask
    for i in range(len(filterList)):
        if filterList[i] == 'opening':
            newmask = opening(newmask, kernel_size, kernel_shape)
            # wenn es opening ist wird in der konsole opening ausgedruckt
        if filterList[i] == 'dilation':
            newmask = dilation(newmask, kernel_size, kernel_shape)
        if filterList[i] == 'closing':
            newmask = closing(newmask, kernel_size, kernel_shape)
        if filterList[i] == 'erosion':
            newmask = erosion(newmask, kernel_size, kernel_shape)

    # gets all connected components
    connectivity = 8
    (numLabels, labels, stats, centroids) = cv2.connectedComponentsWithStats(newmask, connectivity, cv2.CV_32S)
    # centroids = punkte in der mitte, numlabels = anzahl der bälle (z.b bei gelb = 30)
    # goes through all (reasonable) found connected components
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
        print('We have found ' + str(numLabels-numRejected) + ' ' + colorArray[collorNumber].Name + ' balls.')
        found = False
# Satz wird gedruckt wenn alle bedingungen erfüllt sind
    cv2.imshow('Original image', imgcopy)
    cv2.imshow('Masked Image', newmask)

    key = cv2.waitKey(100)
    # 100 millisekunden
    # programm wird beendet
    if key == ord('q'):
        break

    if key == ord('t'):
        imgNumber = imgNumber+1
        (img, height, width, last_dim, imgNumber) = load_Image(imgNumber)
        mask = change_Color()
        found = True
        # damit kann man das bild ändern

    if key == ord('g'):
        imgNumber = imgNumber-1
        (img, height, width, last_dim, imgNumber) = load_Image(imgNumber)
        mask = change_Color()
        found = True
        # damit kann man auf das vorherige bild zugreifen

    if key == ord('e'):
        # damit kann ich die farbe wechseln
        collorNumber = collorNumber+1
        if(collorNumber > len(colorArray)-1):
            collorNumber = 0
        found = True

        hue = colorArray[collorNumber].Hue
        hue_range = colorArray[collorNumber].Hue_Range
        saturation = colorArray[collorNumber].Saturation
        saturation_range = colorArray[collorNumber].Saturation_Range
        value = colorArray[collorNumber].Value
        value_range = colorArray[collorNumber].Value_Range
        filterList = colorArray[collorNumber].Filter
        shape = colorArray[collorNumber].Shape
        expected_roundness = colorArray[collorNumber].Roundness

        mask = change_Color()
        # variablen werden festgelegt

    if key == ord('n'):
        print('Hue: '+str(hue))
        print('Hue-Range : '+str(hue_range))
        print('Saturation : '+str(saturation))
        print('Saturation-Range : '+str(saturation_range))
        print('Value: '+str(value))
        print('Value-Range : '+str(value_range))
        print('Shape : '+str(shape))
        print('Roundness : '+str(expected_roundness))
        print('Filter: '+str(filterList))
        # farbwerte werden ausgedruckt

cv2.destroyAllWindows()
# beendet das programm
