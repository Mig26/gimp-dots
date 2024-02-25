#!/usr/bin/python

from gimpfu import *


def dots(image, layer, visible, dots, dotsize, distribution, scale, invert_scale, fade, invert_fade, coloring, dot_color):
    import subprocess
    import os

    if visible == 0:
        temp = pdb.gimp_image_get_active_drawable(image)
    else:
        temp = pdb.gimp_layer_new_from_visible(image, image, "Visible")
    
    # Create temporary files
    temp_jpeg_path = pdb.gimp_temp_name("jpg")
    temp_png_path = temp_jpeg_path.replace("jpg", "png")
    pdb.file_jpeg_save(image, temp, temp_jpeg_path, temp_jpeg_path, 0.9, 0, 0, 0, "temp", 0, 1, 0, 0)
    
    script_dir = os.path.dirname(os.path.realpath(__file__))
    dots_executable = os.path.join(script_dir, 'dots\dots.exe')
    color_str = ",".join(map(str, dot_color))
    command = [dots_executable, temp_jpeg_path, str(dots), str(dotsize), str(distribution), str(scale), str(invert_scale), str(fade), str(invert_fade), str(coloring), color_str]

    try:
        subprocess.check_call(command)
        
        loaded_image = pdb.file_png_load(temp_png_path, temp_png_path)
        new_layer = pdb.gimp_layer_new_from_drawable(loaded_image.active_layer, image)
        new_layer.name = "Dots"
        image.add_layer(new_layer, -1)
        
    except Exception as e:
        pdb.gimp_message("Failed to run 'dots_exe.exe': {}".format(str(e)))
        return
    gimp.displays_flush()
    # Delete the temporary image files after use
    os.remove(temp_jpeg_path)
    os.remove(temp_png_path)

register(
    "dots",
    "Create a dotted image from source image",
    "Create a dotted image from source image",
    "Mikko Moilanen", "Mikko Moilanen", "2024",
    "<Image>/Filters/Artistic/Dots...",
    "RGB*, GRAY*",  # Image types this script works with
    [
        (PF_RADIO, "visible", "Render from:", 1, (("visible", 1),("current layer",0))),
        (PF_SPINNER, "dots", "Dot density:", 100, (1, 10000, 1)),
        (PF_SPINNER, "dotsize", "Max dot size:", 3, (1, 1000, 1)),
        (PF_RADIO, "distribution", "Dot distribution:", 2, (("random",2),("uniform",1),("pattern",0))),
        (PF_BOOL, "scale", "Scale:", True),
        (PF_BOOL, "invert_scale", "Invert scale:", False),
        (PF_BOOL, "fade", "Fade:", True),
        (PF_BOOL, "invert_fade", "Invert fade:", False),
        (PF_RADIO, "coloring", "Dot coloring:", 1, (("custom",1),("from image",0))),
        (PF_COLOR, "dot_color", "Custom dot color:", (0, 0, 0)),
    ],
    [],
    dots)

main()