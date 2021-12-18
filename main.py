
img = [[[1,1,1],[1,1,1]],[[2,2,2],[2,2,2]]]
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

x = convert2D(img)
print(x)