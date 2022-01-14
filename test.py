import numpy as np
img = [[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[1,1,1],[1,1,1],[1,1,1],[1,1,1]],[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[1,1,1],[1,1,1],[1,1,1],[1,1,1]],[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[1,1,1],[1,1,1],[1,1,1],[1,1,1]],[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[1,1,1],[1,1,1],[1,1,1],[1,1,1]]]
def convert2D(img):
    image= []
    D1 = len(img)
    D2 = len(img[0])
    for i1 in range(D1):
        row = []
        for i2 in range(D2):
            row.append(int((img[i1][i2][0] + img[i1][i2][1]+img[i1][i2][2])/3))
        image.append(row)
    return image

def scaleTo28Pixel(img):
    D1 = len(img)
    D2 = len(img[0])
    ret = []
    img = np.array(img)
    for row in range(0,D1,4):
        matrixRow = []
        for col in range(0,D2,4):
            print(type(img))
            subMatrix = img[row:row+4,col:col+4]
            matrixRow.append(int(np.mean(subMatrix)))
        ret.append(matrixRow)
    return ret


x = convert2D(img)
print(x)
x = scaleTo28Pixel(x)
print(x)
