import sys
import random
from PIL import Image, ImageDraw
import numpy as np


def get_draw_parameters(x, y, dot_max_size, coloring, should_scale, invert_s, should_fade, invert_f, image_gs, image_c, dot_color):
    if coloring == 0:
        color = tuple(image_c[y][x])
    else:
        color = dot_color
    if should_scale:
        dotsize = int(abs(((image_gs[y][x] / 255) * dot_max_size) - dot_max_size))
        if invert_s:
            dotsize = abs(max_dot_size-dotsize)
    else:
        dotsize = dot_max_size
    if should_fade:
        fade = image_gs[y][x] / 255
        if invert_f:
            fade = abs(255-fade)
        col_lst = list(color)
        if len(col_lst) < 4:
            col_lst.append(int(abs((fade * 255) - 255)))
        else:
            col_lst[3] = int(abs((fade * 255) - 255))
        color = tuple(col_lst)
    return [(x-dotsize, y-dotsize), (x+dotsize, y+dotsize)], color


def generate_points(image_path, n, dot_max_size, distribution, scale, invert_s, fade, invert_f, coloring, dot_color):
    with Image.open(image_path) as img:
        image_c = np.asarray(img.convert('RGB'))
        image_gs = np.asarray(img.convert('L'))
        width, height = img.size
    should_scale = scale
    should_fade = fade
    out_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(out_img)
    if distribution == 2:
        n *= 1000
        for i in range(n):
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            coordinates, color = get_draw_parameters(x, y, dot_max_size, coloring, should_scale, invert_s, should_fade, invert_f, image_gs, image_c, dot_color)
            draw.ellipse(coordinates, fill=color)
    else:
        n *= 100
        step = np.sqrt((width * height) / n)
        rows = int(height / step)
        cols = int(width / step)
        adjusted_spacing_x = int(height / rows)
        adjusted_spacing_y = int(width / cols)
        for i in range(n):
            for j in range(n):
                x = int((j + 0.5) * adjusted_spacing_x)
                y = int((i + 0.5) * adjusted_spacing_y)
                if distribution == 0 and i % 2 == 1:
                    x -= int(step / 2)
                if x < width and y < height:
                    coordinates, color = get_draw_parameters(x, y, dot_max_size, coloring, should_scale, invert_s, should_fade, invert_f, image_gs, image_c, dot_color)
                    draw.ellipse(coordinates, fill=color)
    out_path = image_path.replace("jpg", "png")
    out_img.save(out_path, "PNG")


try:
    image_path = sys.argv[1]
    num_dots = int(float(sys.argv[2]))
    max_dot_size = int(float(sys.argv[3]))
    distribution = int(float(sys.argv[4]))
    scale = sys.argv[5] == "True" or sys.argv[5] == "1"
    invert_scale = sys.argv[6] == "True" or sys.argv[5] == "1"
    fade = sys.argv[7] == "True" or sys.argv[6] == "1"
    invert_fade = sys.argv[8] == "True" or sys.argv[5] == "1"
    coloring = int(float(sys.argv[9]))
    r,g,b,a = map(int, sys.argv[10].split(','))
    generate_points(image_path, num_dots, max_dot_size, distribution, scale, invert_scale, fade, invert_fade, coloring, (r, g, b))
except Exception as e:
    pass
