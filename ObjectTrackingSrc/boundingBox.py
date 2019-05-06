

def getPoints(obj, img_width, img_height):
    rel_coords = obj['relative_coordinates']
    width = rel_coords['width'] * img_width
    height = rel_coords['height'] * img_height
    xCen = rel_coords['center_x'] * img_width
    yCen = (1-rel_coords['center_y']) * img_height

    points = makeUniform(width, height, xCen, yCen)
    return points


def makeUniform(width, height, xCen, yCen):
    return (xCen, yCen)


def makeUniform2(width, height, xCen, yCen):
    points = []
    xStart = xCen - width/2
    yStart = yCen - height/2

    for i in range(int(width/10)):
        for j in range(int(height/10)):
            points.append((10*i+xStart,10*j+yStart))

    return points


def makeGaussian(size, fwhm = 3, center=None):
    x=2