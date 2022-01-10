# Music World Sprite Ripper
# Version 1.0
# By Buu342

import os
import sys
import math
import numpy as np
from PIL import Image as im
from pathlib import Path


########################
#       Globals
########################

# Start and end offsets in the uncompressed.pxo where sprites are located
# Values obtained by estimating via 'Image Search Editor'
SPRITE_START = 0x11155C
SPRITE_END   = 0x80CFFC

# Maximum sprite width and heights to prevent the tool from going whack because it mistook random data for an image header
# Values obtained by ripping lots of sprites and then estimating. The largest sprite I found had 514 pixels, so I gave a slightly larger error buffer just in case
SPRITE_MAXW = 600
SPRITE_MAXH = 600

# Image types
IMAGETYPE_1BIT = 0x89
IMAGETYPE_2BIT = 0x8A
IMAGETYPE_4BIT = 0x8B
IMAGETYPE_8BIT = 0x8C


########################
#       Classes
########################

class Header():
    """
    A sprite header class
    """
    def __init__(self):
        self.type     = 0 # 1 byte
        self.width    = 0 # 2 bytes
        self.height   = 0 # 2 bytes
        self.unknown1 = 0 # 1 byte
        self.unknown2 = 0 # 1 byte
        self.unknown3 = 0 # 1 byte
        self.unknown4 = 0 # 1 byte
        self.unknown5 = 0 # 1 byte
        self.pcount   = 0 # 1 byte
        
        
class Color():
    """
    A sprite palette color class
    """
    def __init__(self, red, green, blue):
        self.red   = red
        self.green = green
        self.blue  = blue
    def __repr__(self):
        return ("Color: ["+str(self.red)+", "+str(self.green)+", "+str(self.blue)+"]\n")
        
        
class Image():
    """
    A sprite data class
    """
    def __init__(self):
        self.header  = None
        self.palette = []
        self.texels  = []


########################
#       Functions
########################

def read_header(sprite, f):
    """
    Reads a sprite header and stores it into an Image class
    @param The Image to store the sprite header in
    @param The pointer to the sprite header file to read
    """
    header = Header()

    # Read the header stuff we know
    header.type = f.read(1)[0]
    tmp = (f.read(1)[0]) & 0xFF
    header.width = (((f.read(1)[0]) & 0xFF)<<8) | tmp
    tmp = (f.read(1)[0]) & 0xFF
    header.height = (((f.read(1)[0]) & 0xFF)<<8) | tmp
    
    # Read the unknown bytes
    header.unknown1 = f.read(1)[0]
    header.unknown2 = f.read(1)[0]
    header.unknown3 = f.read(1)[0]
    header.unknown4 = f.read(1)[0]
    header.unknown5 = f.read(1)[0]
    
    # Get the palette count
    header.pcount = f.read(1)[0]
    
    # Set the sprite's header as this one
    sprite.header = header
    
    # Now read the palette
    count = 0
    while count < header.pcount:
        r = f.read(1)[0]
        g = f.read(1)[0]
        b = f.read(1)[0]
        sprite.palette.append(Color(r, g, b))
        count = count + 1
    
    # Finish
    f.close()
    return


def read_image(sprite, f):
    """
    Reads sprite data and stores it into an Image class
    @param The Image to store the data in
    @param The pointer to the sprite data file to read
    """
    count = 0
    size = sprite.header.width * sprite.header.height
    
    # Loop through the image
    if sprite.header.type == IMAGETYPE_1BIT:
        while count < size:
            byte = f.read(1)[0]
            texel1 = ((byte & 0x80) >> 7) & 0xFF
            texel2 = ((byte & 0x40) >> 6) & 0xFF
            texel3 = ((byte & 0x20) >> 5) & 0xFF
            texel4 = ((byte & 0x10) >> 4) & 0xFF
            texel5 = ((byte & 0x08) >> 3) & 0xFF
            texel6 = ((byte & 0x04) >> 2) & 0xFF
            texel7 = ((byte & 0x02) >> 1) & 0xFF
            texel8 = (byte & 0x01) & 0xFF
            sprite.texels.append(texel1)
            sprite.texels.append(texel2)
            sprite.texels.append(texel3)
            sprite.texels.append(texel4)
            sprite.texels.append(texel5)
            sprite.texels.append(texel6)
            sprite.texels.append(texel7)
            sprite.texels.append(texel8)
            count = count + 8
    elif sprite.header.type == IMAGETYPE_2BIT:
        while count < size:
            byte = f.read(1)[0]
            texel1 = ((byte & 0xC0) >> 6) & 0xFF
            texel2 = ((byte & 0x30) >> 4) & 0xFF
            texel3 = ((byte & 0x0C) >> 2) & 0xFF
            texel4 = (byte & 0x03) & 0xFF
            sprite.texels.append(texel1)
            sprite.texels.append(texel2)
            sprite.texels.append(texel3)
            sprite.texels.append(texel4)
            count = count + 4
    elif sprite.header.type == IMAGETYPE_4BIT:
        while count < size:
            byte = f.read(1)[0]
            texel1 = ((byte & 0xF0) >> 4) & 0xFF
            texel2 = (byte & 0x0F) & 0xFF
            sprite.texels.append(texel1)
            sprite.texels.append(texel2)
            count = count + 2
    elif sprite.header.type == IMAGETYPE_8BIT:
        while count < size:
            sprite.texels.append(f.read(1)[0])
            count = count + 1

    # Finish
    f.close()
    return
    
    
def export_image(sprite, name):
    """
    Reads a sprite header and stores it into an Image class
    @param The Image to store the sprite header in
    @param The pointer to the sprite header file to read
    """
    count = 0
    img = im.new('RGB', (sprite.header.width, sprite.header.height))
    size = sprite.header.width * sprite.header.height
    data = []
    
    # Loop through the image and add the data from the palette
    while count < size:
        pal = sprite.palette[sprite.texels[count]]
        data.append((pal.red, pal.green, pal.blue))
        count = count + 1
        
    # Create the exported folder if it doesn't exist
    if (not os.path.exists("Converted")):
        os.mkdir("Converted")
    
    # Export the image
    img.putdata(data)
    img.save("Converted/"+name+'.png')
    print("Exported '"+name+".png'")
    return
    
    
def convert_sprite(fheader_path, fimage_path):
    """
    Takes in a filepath for a sprie header and sprite data file and exports it as a PNG.
    @param The filepath of the sprite header file
    @param The filepath of the sprite data file
    """
    fheader = None
    fimage = None
    sprite = Image()
    
    # Open the header file
    try:
        fheader = open(fheader_path, "rb")
    except:
        print('Problem opening file \''+sys.argv[1]+'\'')
        sys.exit()
        
    # Open the image file
    try:
        fimage = open(fimage_path, "rb")
    except:
        print('Problem opening file \''+sys.argv[1]+'\'')
        sys.exit()
    
    # Read the files into our struct
    read_header(sprite, fheader)
    read_image(sprite, fimage)
    
    # Export the image
    export_image(sprite, Path(fimage_path).stem)
    return
    
    
def rip_sprites(pxo_path):
    """
    Takes in an uncompressed Music World PXO and rips out all the sprites it finds
    @param The filepath of the Music World PXO
    """
    count = 0
    fpxo = None
    
    # Open the uncompressed PXO file
    try:
        fpxo = open(pxo_path, "rb")
    except:
        print('Problem opening file \''+sys.argv[1]+'\'')
        sys.exit()
        
    # Ensure it's actually uncompressed
    header = fpxo.read(4)
    if (chr(header[0]) != 'P' or chr(header[1]) != 'X' or chr(header[2]) != 'O' or chr(header[3]) != '4'):
        print("Error: This is not an uncompressed PXO")
        sys.exit()
        
    # Create a folder for us to dump the sprites to, and then jump to the start of the sprites
    if (not os.path.exists("Ripped")):
        os.mkdir("Ripped")
    fpxo.seek(SPRITE_START)
    
    # Now start ripping and dumping into the ripped folder
    while fpxo.tell() < SPRITE_END:
        start = fpxo.tell()
        
        # Get the image type
        type = fpxo.read(1)[0]
        
        # First, check if the image header is valid
        if (type < IMAGETYPE_1BIT or type > IMAGETYPE_8BIT):
            continue
            
        name_header  = "Ripped/"+str(count).zfill(4)+"_header.bin"
        name_imgdata = "Ripped/"+str(count).zfill(4)+".bin"
        
        # Get image width and height
        tmp = (fpxo.read(1)[0]) & 0xFF
        width = (((fpxo.read(1)[0]) & 0xFF)<<8) | tmp
        tmp = (fpxo.read(1)[0]) & 0xFF
        height = (((fpxo.read(1)[0]) & 0xFF)<<8) | tmp
        
        # If the image is too big or small, it's probably not a sprite
        if (width > SPRITE_MAXW or height > SPRITE_MAXH or width == 0 or height == 0):
            continue
            
        # Skip unknown bytes
        fpxo.read(5)
        
        # Get the palette count, and check if it's valid for the image type
        pcount = fpxo.read(1)[0]
        if (pcount == 0):
            continue
        if (type == IMAGETYPE_1BIT):
            if (pcount > 2):
                continue
        elif (type == IMAGETYPE_2BIT):
            if (pcount > 4):
                continue
        elif (type == IMAGETYPE_4BIT):
            if (pcount > 16):
                continue
        print("Found sprite "+str(count).zfill(4)+" at "+hex(start)+". Type = "+hex(type)+", "+str(width)+"x"+str(height)+", "+str(pcount)+" colors.")
        
        # Calculate the image size (in bytes)
        if (type == IMAGETYPE_1BIT):
            size = math.ceil(width*height/8)
        elif (type == IMAGETYPE_2BIT):
            size = math.ceil(width*height/4)
        elif (type == IMAGETYPE_4BIT):
            size = math.ceil(width*height/2)
        elif (type == IMAGETYPE_8BIT):
            size = width*height
            
        # Create the header file binary
        fpxo.seek(start)
        fout = open(name_header, 'wb')
        data = bytearray(fpxo.read(11+pcount*3))
        fout.write(data)
        fout.close()
        fout = open(name_imgdata, 'wb')
        data = bytearray(fpxo.read(size))
        fout.write(data)
        fout.close()
        count = count + 1
    
    # Finished
    print("Finished dumping sprites")
    return


def main():
    """
    Program entrypoint
    """
    print('Music World Converter')
    
    # Check for command line arguments
    if (len(sys.argv) < 2 or len(sys.argv) > 3):
        print('Usage: <uncompressed.pxo>')
        print('or')
        print('Usage: <folder of .bin files>')
        print('or')
        print('Usage: <header.bin> <image.bin>')
        sys.exit()
    
    # Pick what to do based on the command line arguments
    if (len(sys.argv) == 2):
        if (not os.path.isdir(sys.argv[1])):
            # Rip all the sprites from an uncompressed pxo
            rip_sprites(sys.argv[1]) 
        else:
            # Convert all the sprites in a folder
            files = os.listdir(sys.argv[1])
            count = 0
            while count < len(files):
                convert_sprite(sys.argv[1]+"/"+files[count+1], sys.argv[1]+"/"+files[count])
                count = count + 2
    elif (len(sys.argv) == 3):
        # Convert a single sprite
        convert_sprite(sys.argv[1], sys.argv[2]) 


########################
#  Program Entrypoint
########################

main()