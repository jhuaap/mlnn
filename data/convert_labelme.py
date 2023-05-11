import PIL
import json
import numpy
from PIL import Image, ImageDraw
import os
import glob

jsons = glob.glob('*.json') + glob.glob('*.json')

def draw(json_name):
    prefix, _ = os.path.splitext(json_name)
    print(prefix)

    with open(json_name) as f:
        poly = json.load(f)

    img2 = Image.new('L', (poly['imageWidth'], poly['imageHeight']), 0)
    for shape in poly['shapes']:
        ImageDraw.Draw(img2).polygon([tuple(point) for point in shape['points']], outline=255, fill=255)
    img2.save(prefix + '_mask.png', format='png')