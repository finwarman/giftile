#! /usr/bin/env python3

# Tool to rsize a gif, then split it into 20x20 px tiles

from math import floor, fabs
from PIL import Image, ImageSequence


def resize_image(original_img, crop_w, crop_h):
    img_w, img_h = (original_img.size[0], original_img.size[1])
    n_frames = getattr(original_img, 'n_frames', 1)

    def resize_frame(frame):
        return frame.resize((crop_w, crop_h), Image.ANTIALIAS)

    # single frame
    if n_frames == 1:
        return resize_frame(original_img)
    # multi-frame image
    else:
        frames = []
        for frame in ImageSequence.Iterator(original_img):
            frames.append(resize_frame(frame))
        return frames


def generate_tile(original_img, origin_x, origin_y, tile_width):
    n_frames = getattr(original_img, 'n_frames', 1)

    def crop_tile(frame):
        return frame.crop((origin_x, origin_y, origin_x + tile_width, origin_y + tile_width))

    # single frame
    if n_frames == 1:
        return crop_tile(original_img)
    # multi-frame image
    else:
        frames = []
        for frame in ImageSequence.Iterator(original_img):
            frames.append(crop_tile(frame))
        return frames


im = Image.open("files/input.gif")
im.seek(im.tell() + 1)  # loads all frames

hres = 60  # px
vres = 30  # px
tile_size = 15  # square px

print("Resizing input image...")

duration = im.info['duration']
frames = resize_image(im, hres, vres)

frames[0].save("files/out.gif",
               save_all=True,
               append_images=frames[1:],
               optimize=False,
               duration=duration, loop=0
               )

print("Done!")

im = Image.open("files/out.gif")

tiles_width = hres // tile_size
tiles_height = vres // tile_size

print("Generating tiles ({} images): {} wide, {} tall".format(
    tiles_width*tiles_height, tiles_width, tiles_height))

for x in range(tiles_width):
    for y in range(tiles_height):
        originX = x * tile_size
        originY = y * tile_size
        filename = "tile_r{}_c{}".format(y, x)

        tile_frames = generate_tile(im, originX, originY, tile_size)
        tile_frames[0].save("files/tiles/{}.gif".format(filename),
                            save_all=True,
                            append_images=tile_frames[1:],
                            optimize=False,
                            duration=duration, loop=0
                            )

print("Done!")
