import matplotlib.pyplot as plt
import numpy as np

from PIL import Image

def getColorClusterKey(r, g, b):
    cluster_factor = 32
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
        rgb += i + '7'
    return rgb


def keyToRGB(color):
    r = int(color[0], 16)*16
    g = int(color[1], 16)*16
    b = int(color[2], 16)*16
    return tuple((r, g, b))


firstImg = Image.open("../images/fly.png")
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
    if i % firstImg.width == 0:
        last_pixel = pixel
    else:
        last_pixel = oldImgData[i - 1]

    if i > firstImg.width:
        last_row_pixel = oldImgData[i]
    else:
        last_row_pixel = oldImgData[i - firstImg.width]

    orgColorKey = getColorClusterKey(pixel[0], pixel[1], pixel[2])
    last_cluster = getColorClusterKey(last_pixel[0], last_pixel[1], last_pixel[2])
    last_row_cluster = getColorClusterKey(last_row_pixel[0], last_row_pixel[1], last_row_pixel[2])

    if last_cluster != orgColorKey:
        color = (0, 0, 0)
    elif last_row_cluster != orgColorKey:
        color = (0, 0, 0)
    else:
        color = (255, 255, 255)
    newImgData.append(color)

# for i in range(len(newImgData)):
#     if newImgData[i] == (255, 255, 255):
#         continue
#     j = 1
#
#     best = None
#     while (j + i) % firstImg.width != 0:
#         for k in range(j + 1):
#             bot = i + j + k * firstImg.width
#             top = i + j - k * firstImg.width
#             if 0 < top < len(newImgData) and newImgData[top] == (0, 0, 0):
#                 best = -k
#                 break
#             if bot < len(newImgData) and newImgData[bot] == (0, 0, 0):
#                 best = k
#                 break
#
#         if best is not None:
#             break
#         j += 1
#
#     if best is None:
#         continue
#
#     tmp = j - abs(k)
#     ks = 1
#     if k < 0:
#         ks = -1
#     if tmp > 0:
#         for m in range(tmp):
#             newImgData[i + m] = (0, 0, 0)
#         for m in range(abs(k)):
#             try:
#                 newImgData[i + tmp + m + ks * m * firstImg.width] = (0, 0, 0)
#             except:
#                 pass
#     else:
#         tmp = -tmp
#         for m in range(abs(k)):
#             try:
#                 newImgData[i + m + ks * m * firstImg.width] = (0, 0, 0)
#             except:
#                 pass
#         for m in range(tmp):
#                 newImgData[i + abs(k) + m * ks * firstImg.width] = (0, 0, 0)


                    # for m in range(tmp):
        #     newImgData[i + m] = (0, 0, 0)


newImg = Image.new('RGB', firstImg.size)
newImg.putdata(newImgData)
newImg.show()
# newImg.save('../images/result_rgb.png')
# plotBarX(list(firstImgDict.keys()), list(firstImgDict.values()))
# plotBarX(list(secondImgDict.keys()), list(secondImgDict.values()))