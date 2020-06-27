from PIL import Image

img = Image.open('../images/edges.png')
img = img.convert("RGBA")
datas = img.getdata()

newData = []
for item in datas:
    (R, G, B, A) = item
    Y = 0.2126*R + 0.7152*G + 0.0722*B

    if Y > 240:
        newData.append((255, 255, 255, 0))
    else:
        newData.append(item)

img.putdata(newData)
img.save("../images/edges_transparent.png", "PNG")