import os
from PIL import ImageFont


def get_a_font_object(font='roboto', size=30):
    """ Try to create a font object. get a default robot if failed """
    FONTS_DIR = os.environ.get('FONTS_DIR')

    if (font+'.ttf') in os.listdir(FONTS_DIR):
        font_path = f'{FONTS_DIR}{font}.ttf'
        font_object = ImageFont.truetype(font_path, size)
    else:
        font_path = f'{FONTS_DIR}roboto.ttf' # Default font
        font_object = ImageFont.truetype(font_path, size)
    return font_object
