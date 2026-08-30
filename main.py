import os, sys
from PIL import Image


# Pseudocode from Wikipedia
# for each y
#    for each x
#       oldpixel        := pixel[x][y]
#       newpixel        := find_closest_palette_color (oldpixel)
#       pixel[x][y]     := newpixel
#       quant_error     := oldpixel - newpixel
#       pixel[x+1][y  ] := pixel[x+1][y  ] + quant_error * 7 / 16
#       pixel[x-1][y+1] := pixel[x-1][y+1] + quant_error * 3 / 16
#       pixel[x  ][y+1] := pixel[x  ][y+1] + quant_error * 5 / 16
#       pixel[x+1][y+1] := pixel[x+1][y+1] + quant_error * 1 / 16

def distSquared(a,b):
  return (a[0]-b[0])*(a[0]-b[0])+(a[1]-b[1])*(a[1]-b[1])+(a[2]-b[2])*(a[2]-b[2])

def find_closest_palette_color(pixel, palette):
  best_color = (0,0,0)
  for r,g,b in palette:
    if distSquared(pixel,(r,g,b)) < distSquared(pixel,best_color):
      best_color=(r,g,b)
  return best_color

def get_quant_error(oldPixel,newPixel):
  dr=oldPixel[0]-newPixel[0]
  dg=oldPixel[1]-newPixel[1]
  db=oldPixel[2]-newPixel[2]
  return (dr, dg, db)

def mult_tuple(tup,mult):
  return (int(tup[0]*mult),int(tup[1]*mult),int(tup[2]*mult))

def add_tuple(tup1,tup2):
  return (tup1[0]+tup2[0],tup1[1]+tup2[1],tup1[2]+tup2[2])

def main():
  if len(sys.argv) != 4:
    print(f"Usage:\npython3 {sys.argv[0]} <path/to/image.png> <number of colors> <path/to/output.png>")
    exit(0)
  with Image.open(sys.argv[1]) as image:
    numColors:int = int(sys.argv[2])
    quantized_image = image.quantize(numColors)
    palette = quantized_image.getpalette()
    colors:list[tuple[int,int,int]] = []
    for i in range(0,len(palette),3):
      colors.append((palette[0+i],palette[1+i],palette[2+i]))
    pixels = image.load()
    width=image.size[0];
    height=image.size[1];
    for y in range(height):
      for x in range(width):
        old_pixel = pixels[x,y]
        new_pixel = find_closest_palette_color(pixels[x,y],colors)
        pixels[x,y] = new_pixel
        quant_error = get_quant_error(new_pixel,old_pixel)
        if x+1<width:
          pixels[x+1, y  ] = add_tuple(pixels[x+1, y  ], mult_tuple(quant_error,7 / 16))
        if x-1>0 and y+1<height:
          pixels[x-1, y+1] = add_tuple(pixels[x-1, y+1], mult_tuple(quant_error,3 / 16))
        if y+1<height:
          pixels[x  , y+1] = add_tuple(pixels[x  , y+1], mult_tuple(quant_error,5 / 16))
        if x+1<width and y+1<height:
          pixels[x+1, y+1] = add_tuple(pixels[x+1, y+1], mult_tuple(quant_error,1 / 16))



    image.save(sys.argv[3])

  return 0



main()
