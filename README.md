
# Music World Sprite Dumper
This repository contains a python script reads an UNCOMPRESSED Music World pxo file and attempts to dump sprites from it. The tool is not 100% correct, but I think it rips everything out correctly... 

I had to make some assumptions about the data itself (specifically `SPRITE_MAXW/H`) because of the fact that data is not packed how I think it is. There's some stray bytes that I haven't been able to figure out what they are yet, probably because I haven't correctly figured out the sprite headers. This might be fixed in a future date.


### Prerequisites
First, you need to have Python 3 installed, there's [online guides](https://realpython.com/installing-python/) for doing that if you don't know how.

Next, you'll need a copy of the Music World PXO. You can either rip this from your own phone, or find one online. I won't provide those for you.

Finally, you will need to uncompress the PXO. This can be done using a tool such as [LGUI](https://code.google.com/archive/p/lgui/).

Once you have all of those steps done, you can start ripping out sprites.


### Program usage
The program has three modes of operation:

##### Rip from PXO
This will rip all sprites that it finds from an uncompressed Music World PXO. The ripped sprites will be dumped to a folder called "Ripped", which will contain the sprite headers and the sprites themselves in the proprietary format used by Music World.
```
python mwsripper.py <Uncompressed PXO>
```

##### Convert sprite to PNG
This mode will take a single sprite and its header and convert it to a PNG. The PNG will be dumped to a folder called "Converted", and the PNG itself will have the same name as the data file.
```
python mwsripper.py <Sprite Header> <Sprite Data>
```

##### Convert folder of rips to PNG
This mode will read an entire folder of sprite rips and convert them to PNG. The outputted PNGs will be dumped to a folder called "Converted". This mode does no error checking, it assumes everything inside a folder is a sprite+header file combo. This is best used with a folder that was ripped using the [Rip from PXO](#Rip_from_PXO) mode.
```
python mwsripper.py <Folder with sprite data and headers>
```

### Problems
Besides what was outlined in the very top of the README, I am not aware of any major bugs with the script. If any arise, please open [an issue](../../issues).


### Future work
Currently this script only rips sprites. It can probably be extended in the future to rip out music MIDI's, WAVs, and possibly any other data which can be found (which I have already ripped out manually since they weren't in any proprietary format). Maybe I could potentially expand it to also decompress a given PXO.
