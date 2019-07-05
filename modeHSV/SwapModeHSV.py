import matplotlib.pyplot as plt
import numpy as np
import colorsys

from PIL import Image

max_cluster_no = 512


def getColorClusterKey(r, g, b):
    (h, s, v)= colorsys.rgb_to_hsv(r, g, b)
    h = int(h*max_cluster_no)/max_cluster_no
    temp = colorsys.hsv_to_rgb(h, 1, 255)
    key = '#%02x%02x%02x' % (int(temp[0]), int(temp[1]), int(temp[2]))
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
        barslist[i].set_color(label[i])
    plt.show()


def keyToRGB(colorString):
    temp = colorString.lstrip('#')
    return tuple(int(temp[p:p+2], 16) for p in (0, 2, 4))


firstImg = Image.open("../images/fly.png")
firstImgDict = {}

for pixel in firstImg.getdata():
    colorHit(colorClusterKey=getColorClusterKey(pixel[0], pixel[1], pixel[2]),
             imgClusterDict=firstImgDict)

secondImg = Image.open("../images/flr.png")
secondImgDict = {}

for pixel in secondImg.getdata():
    colorHit(colorClusterKey=getColorClusterKey(pixel[0], pixel[1], pixel[2]),
             imgClusterDict=secondImgDict)

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

newImgData =[]
for pixel in firstImg.getdata():
    h_original, s_original, v_original = colorsys.rgb_to_hsv(pixel[0], pixel[1], pixel[2])
    baseColorKey = getColorClusterKey(pixel[0], pixel[1], pixel[2])
    rgb_base = keyToRGB(baseColorKey)
    h_base, s_base, v_base = colorsys.rgb_to_hsv(rgb_base[0], rgb_base[1], rgb_base[2])
    diff_org_base = h_original - h_base

    mapColorKey = mapColors[baseColorKey]
    color = keyToRGB(mapColorKey)

    hsvColor = colorsys.rgb_to_hsv(color[0], color[1], color[2])

    rgbColor = colorsys.hsv_to_rgb(hsvColor[0] + diff_org_base, (hsvColor[1]+s_original)/2, (hsvColor[2]+v_original)/2)
    newImgData.append((int(rgbColor[0]), int(rgbColor[1]), int(rgbColor[2])))

newImg = Image.new('RGB', firstImg.size)
newImg.putdata(newImgData)
newImg.show()
newImg.save('../images/result_hsv.png')
# plotBarX(list(firstImgDict.keys()), list(firstImgDict.values()))
# plotBarX(list(secondImgDict.keys()), list(secondImgDict.values()))