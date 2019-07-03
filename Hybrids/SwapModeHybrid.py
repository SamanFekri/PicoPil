import matplotlib.pyplot as plt
import numpy as np

from PIL import Image
import colorsys


def getColorClusterKey(r, g, b):
    key = ''
    key += format(int(r / 16), 'x')
    key += format(int(g / 16), 'x')
    key += format(int(b / 16), 'x')
    return key


def colorHit(colorClusterKey, imgClusterDict):
    if colorClusterKey in imgClusterDict:
        imgClusterDict[colorClusterKey] += 1
    else:
        imgClusterDict[colorClusterKey] = 1


def plotBarX(label, value):
    # this is for plotting purpose
    index = np.arange(len(label))
    plt.figure(figsize=(20, 5))  # width:20, height:3
    barslist = plt.bar(index, value, align='edge', width=0.3)
    plt.xlabel('Cluster key', fontsize=5)
    plt.ylabel('Hit Cluster', fontsize=5)
    plt.tick_params(
        axis='x',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom=False,  # ticks along the bottom edge are off
        top=False,  # ticks along the top edge are off
        labelbottom=False)  # labels along the bottom edge are off
    plt.title('Image color cluster hit')
    for i in range(len(barslist)):
        barslist[i].set_color(clusterToRGB(label[i]))
    plt.show()


def clusterToRGB(color):
    rgb = '#'
    for i in color:
        rgb += i + '7'
    return rgb


def keyToRGB(color):
    r = int(color[0], 16) * 16
    g = int(color[1], 16) * 16
    b = int(color[2], 16) * 16
    return tuple((r, g, b))


firstImg = Image.open("../images/fly.png")
firstImgDict = {}
firstMean = {'s': 0.0, 'v': 0.0}
for pixel in firstImg.getdata():
    colorHit(colorClusterKey=getColorClusterKey(pixel[0], pixel[1], pixel[2]),
             imgClusterDict=firstImgDict)
    h, s, v = colorsys.rgb_to_hsv(pixel[0], pixel[1], pixel[2])
    firstMean['s'] += s
    firstMean['v'] += v

n = len(firstImg.getdata())
firstMean['s'] /= n
firstMean['v'] /= n

secondImg = Image.open("../images/flr.png")
secondImgDict = {}
secondMean = {'s': 0.0, 'v': 0.0}
for pixel in secondImg.getdata():
    colorHit(colorClusterKey=getColorClusterKey(pixel[0], pixel[1], pixel[2]),
             imgClusterDict=secondImgDict)
    h, s, v = colorsys.rgb_to_hsv(pixel[0], pixel[1], pixel[2])
    secondMean['s'] += s
    secondMean['v'] += v

n = len(secondImg.getdata())
secondMean['s'] /= n
secondMean['v'] /= n

diffMean = {'s': secondMean['s'] - firstMean['s'], 'v': secondMean['v'] - firstMean['v']}

firstImgColorSorted = sorted(firstImgDict.items(), key=lambda kv: kv[1], reverse=True)
firstImgDict = {}
for i in range(len(firstImgColorSorted)):
    firstImgDict[firstImgColorSorted[i][0]] = firstImgColorSorted[i][1]

secondImgColorSorted = sorted(secondImgDict.items(), key=lambda kv: kv[1], reverse=True)
secondImgDict = {}
for i in range(len(secondImgColorSorted)):
    secondImgDict[secondImgColorSorted[i][0]] = secondImgColorSorted[i][1]

mapColors = {}
for i in range(len(firstImgColorSorted)):
    if i < len(secondImgColorSorted):
        mapColors[firstImgColorSorted[i][0]] = secondImgColorSorted[i][0]
    else:
        mapColors[firstImgColorSorted[i][0]] = secondImgColorSorted[-1][0]

newImgData = []
for pixel in firstImg.getdata():
    orgColorKey = getColorClusterKey(pixel[0], pixel[1], pixel[2])
    #
    org_h, org_s, org_v = colorsys.rgb_to_hsv(pixel[0], pixel[1], pixel[2])
    #
    mapColorKey = mapColors[orgColorKey]
    color = keyToRGB(mapColorKey)
    #
    sec_h, sec_s, sec_v = colorsys.rgb_to_hsv(color[0], color[1], color[2])
    #
    secRGB = colorsys.hsv_to_rgb(sec_h, org_s + diffMean['s'], org_v + diffMean['v'])
    color = (int(secRGB[0]), int(secRGB[1]), int(secRGB[2]))
    newImgData.append(color)

newImg = Image.new('RGB', firstImg.size)
newImg.putdata(newImgData)
newImg.show()

# plotBarX(list(firstImgDict.keys()), list(firstImgDict.values()))
# plotBarX(list(secondImgDict.keys()), list(secondImgDict.values()))
