import math
import PIL.Image as Image
import PIL.ImageGrab as ImageGrab
import matplotlib.pyplot as plot
import aircv as ac
import sys


if len(sys.argv) > 1:
    print("输入图片：" + sys.argv[1])
    inputImg = sys.argv[1]
else:
    # 保存剪切板内图片
    im = ImageGrab.grabclipboard()
    if isinstance(im, Image.Image):
        print("使用剪切板图片：clipboard.png")
        im.save("clipboard.png")
        inputImg = "clipboard.png"
    elif im:
        for filename in im:
            print("使用剪切板图片：" + filename)
            inputImg = filename
    else:
        print("没有指定图片，使用 input.jpg")
        inputImg = "input.jpg"


# imgsrc=原始图像，imgobj=待查找的图⽚
def matchImg(imgsrc, imgobj, confidencevalue=0.3):
    imsrc = ac.imread(imgsrc)
    imobj = ac.imread(imgobj)
    match_result = ac.find_template(imsrc, imobj, confidencevalue)

    if match_result is not None:
        match_result['shape'] = (imsrc.shape[1], imsrc.shape[0])  # 0为⾼，1为宽
    return match_result["result"]


image = Image.open(inputImg)
# 大小/尺寸
imgSize = image.size
# 图片的宽
width = image.width
# 图片的高
height = image.height

# 小孩 boy(64,782) -> (64,220)
# boy_x = 100
# boy_y = 220
res = matchImg(inputImg, "boy.jpg")
boy_x = int(res[0]) + 30
boy_y = height - res[1]

# 天花板 ceiling(x,110) -> (x,892)
# ceiling_y = 892
res = matchImg(inputImg, "ceiling.jpg")
ceiling_y = height - res[1] - boy_y

# 篮筐 hoop(480,465) -> (480,537)
# hoop_x = 480
# hoop_y = 537
res = matchImg(inputImg, "hoop.jpg")
hoop_x = int(res[0]) - boy_x
hoop_y = height - res[1] - boy_y

img = plot.imread(inputImg)
fig, ax = plot.subplots()
# 指定图片的高度和宽度
ax.imshow(img, extent=[- boy_x, width - boy_x, - boy_y, height - boy_y])

# 根据抛物线经过篮筐(a,b) 天花板(?,c) 求出对称轴 d = ?
a = hoop_x
b = hoop_y
c = ceiling_y
print("小孩：(0,0)")
print("天花板：(d," + str(c) + ")")
print("篮筐：(" + str(a) + "," + str(b) + ")")
plot.plot(hoop_x, hoop_y, 'r*')
d = (a * c - a * math.sqrt(c * c - b * c)) / b
print("求得对称轴：d = " + str(d))
plot.plot(d, c, 'r*')

x = []
y = []
for x1 in range(0, hoop_x + 1):
    y1 = c - c * (x1 - d) * (x1 - d) / d / d
    if y1 < 0:
        break
    x.append(x1)
    y.append(y1)
plot.plot(x, y)
plot.savefig("./result.jpg")
print("输出图片：result.jpg")
plot.show()
