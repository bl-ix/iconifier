"""
Generate icns files from a directory of PNGs.

"""

import os
import sys
from PIL import Image
import pathlib


def export_based_on_dimensions(png_file):
    img = Image.open(png_file)
    sizes_for_2x = [1024, 512, 256, 32]
    export_dir = f'{png_file.parts[0]}{"/".join(png_file.parts[1:-2])}/' \
                 f'{png_file.parts[-2]}_iconset/'
    if not pathlib.Path(export_dir).exists():
        import os
        os.mkdir(export_dir)

    # if size is 1024, then its 512x512@2x

    if img.size[0] == 1024:
        file_name = 'icon_512x512@2x.png'
    elif img.size[0] in sizes_for_2x:
        base_size = str(int(img.size[0]/2))
        filename = f'{export_dir}icon_{base_size}x{base_size}@2x.png'
        img.save(f'{export_dir}icon_{base_size}x{base_size}@2x.png')
        # print(f'Saved {export_dir}icon_{base_size}x{base_size}@2x.png')



    # export it anyway
    img.save(f'{export_dir}icon_{img.size[0]}x{img.size[0]}.png')
    print(f'Saved {export_dir}icon_{img.size[0]}x{img.size[0]}.png')

    if img.size[0] == 32:
        img.resize((16, 16)).save(f'{export_dir}icon_16x16.png')

    return export_dir


def rename_to_iconset(export_dir):
    os.rename(export_dir[:-1], f'{export_dir[:-9]}.iconset')
    return f'{export_dir[:-9]}.iconset'


def convert_to_icns(iconset_file):
    import subprocess

    cmd = ['iconutil', '-c', 'icns', iconset_file]
    return_code = subprocess.call(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if return_code:
        return False
    else:
        return True

def main(directory):
    # list the items in the directory
    from os import listdir

    # determine which are pngs
    png_files = [file for file in pathlib.Path(directory).iterdir() if file.is_file() and
                 file.suffix == '.png']

    export_dir = [export_based_on_dimensions(png_file) for png_file in png_files][0]
    iconset_file = rename_to_iconset(export_dir)

    icon_ready = convert_to_icns(iconset_file)
    if icon_ready:
        import shutil
        shutil.rmtree(iconset_file)
    print(f'Icon created.')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main('path/to/directory')
