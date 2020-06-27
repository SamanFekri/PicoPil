from PIL import Image

img = Image.open('../images/edges.png')
img = img.convert("RGBA")
datas = img.getdata()

img2 = Image.open('../images/chandler.png')
img2 = img2.convert("RGBA")
datas2 = img2.getdata()

newData = []
for (i, item) in enumerate(datas):
    (R, G, B, A) = item
    Y = 0.2126 * R + 0.7152 * G + 0.0722 * B
    if Y > 240:
        newData.append(datas2[i])
    else:
        item = list(int((Y/255.0) * x) for x in datas2[i])
        item[3] = 255
        newData.append(tuple(item))

img.putdata(newData)
img.save("../images/chandler_art.png", "PNG")
