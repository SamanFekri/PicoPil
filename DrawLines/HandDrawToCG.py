import matplotlib.pyplot as plt
import numpy as np

from PIL import Image

def getColorClusterKey(r, g, b):
    cluster_factor = 16
    key = ''
    key += format(int(r / cluster_factor), 'x')
    key += format(int(g / cluster_factor), 'x')
    key += format(int(b / cluster_factor), 'x')
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
        rgb += i
    return rgb


def keyToRGB(color):
    r = int(color[0], 16)*16
    g = int(color[1], 16)*16
    b = int(color[2], 16)*16
    return tuple((r, g, b))


firstImg = Image.open("../images/supernova.jpg")
firstImgDict = {}

for pixel in firstImg.getdata():
    colorHit(colorClusterKey=getColorClusterKey(pixel[0], pixel[1], pixel[2]),
             imgClusterDict=firstImgDict)

firstImgColorSorted = sorted(firstImgDict.items(), key=lambda kv: kv[1], reverse=True)
firstImgDict = {}
for i in range(len(firstImgColorSorted)):
    firstImgDict[firstImgColorSorted[i][0]] = firstImgColorSorted[i][1]

newImgData =[]
oldImgData = firstImg.getdata()
for i in range(len(oldImgData)):
    pixel = oldImgData[i]
    if pixel[0] > 128 or pixel[1] > 128 or pixel[2] > 128:
        newImgData.append((255, 255, 255))
    else:

        newImgData.append((0, 0, 0))

    # newImgData.append(color)

newImg = Image.new('RGB', firstImg.size)
newImg.putdata(newImgData)
newImg.show()
newImg.save('../images/result_hdtocg.png')