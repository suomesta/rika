"""Convert RGBA data into HTML string.

create_table() converts RGB data into HTML table string.
create_canvas() converts RGBA data into HTML canvas string.

create_table_by_pil() is wrapper of create_table(), it converts image file
name into HTML table string using PIL.
create_canvas_by_pil() is wrapper of create_canvas(), it converts image file
name into HTML canvas string using PIL.
"""

from itertools import islice
import sys

__author__ = 'suomesta'
__version__ = '1.0.0'

# -------->>-------->>-------->>-------->>-------->> constants

PIL_IMPORT_ERROR = __file__ + """\
 requires Pillow (PIL).\nSee https://pypi.org/project/Pillow/\n"""

ARGPARSE_DESCRIPTION = """\
Output image string in HTML.
If --id is set, then <canvas> image string is output.
Otherwise, <table> is output."""

TABLE_START = """\
<table border=0 cellpadding=0 cellspacing=0 width={0} height={1}>"""

TR_START = """\
<tr height=1>"""

TD_WITH_WIDTH = """\
<td width=1 bgcolor=#{0:02x}{1:02x}{2:02x}></td>"""

TD_NO_WIDTH = """\
<td bgcolor=#{0:02x}{1:02x}{2:02x}></td>"""

TR_END = """\
</tr>"""

TABLE_END = """\
</table>"""

CANVAS_1_HALF = (
    '<canvas id="{0}" width="{1}" height="{2}"></canvas>'
    '<script>'
    'let canvas = document.getElementById("{0}");'
    'let context = canvas.getContext("2d");'
    'let imageData = context.createImageData(canvas.width, canvas.height);'
    'let tmp = ['
)

CANVAS_2_HALF = (
    '];'
    'for (let i = 0; i < tmp.length; i++) {'
    'imageData.data[i] = tmp[i];'
    '}'
    'context.putImageData(imageData, 0, 0);'
    '</script>'
)

# -------->>-------->>-------->>-------->>-------->> private


def _create_td(j, width, rgb_obj):
    """Do yield <td>...</td> string data."""
    td_str = TD_WITH_WIDTH if j == 0 else TD_NO_WIDTH
    rgbs = islice(rgb_obj, j * width, (j + 1) * width)
    yield from (td_str.format(*rgb) for rgb in rgbs)


def _create_tr(width, height, rgb_obj):
    """Do yield <tr>...</tr> string data."""
    for j in range(height):
        yield TR_START
        yield from _create_td(j, width, rgb_obj)
        yield TR_END


def _create_pixels(size, rgba_obj, has_alpha):
    """Do yield 'r,g,b,a' or 'r,g,b,255'."""
    fmt = '{0},{1},{2},{3}' if has_alpha else '{0},{1},{2},255'
    yield from (fmt.format(*i) for i in rgba_obj)

# -------->>-------->>-------->>-------->>-------->> public


def create_table(width, height, rgb_obj):
    """Convert RGB data into HTML table string.

    param[in]  width: Width of image. in int.
    param[in]  height: Height of image. in int.
    param[in]  rgb_obj: RGB object. Its size should be width * height.
                        rgb_obj[i][0] should be red value,
                        rgb_obj[i][1] should be green value,
                        rgb_obj[i][2] should be blue value.
    yield      created string '<table>...</table>'.
               ''.join(create_table(...)) is a good way to use output.
    """
    yield TABLE_START.format(width, height)
    yield from _create_tr(width, height, rgb_obj)
    yield TABLE_END


def create_canvas(canvas_id, width, height, rgba_obj, has_alpha):
    """Convert RGBA data into HTML5 canvas string.

    param[in]  canvas_id: Id of canvas tag. in str.
    param[in]  width: Width of image. in int.
    param[in]  height: Height of image. in int.
    param[in]  rgba_obj: RGBA (or RGB) object. Its size should be
                         width * height.
                         rgba_obj[i][0] should be red value,
                         rgba_obj[i][1] should be green value,
                         rgba_obj[i][2] should be blue value,
                         optional rgba_obj[i][3] should be alpha value.
    param[in]  has_alpha: True indicates to support RGB and A.
    yield      created string '<canvas>...</canvas><script>...</script>'.
               ''.join(create_table(...)) is a good way to use output.
    """
    yield CANVAS_1_HALF.format(canvas_id, width, height)
    yield ','.join(_create_pixels(width * height, rgba_obj, has_alpha))
    yield CANVAS_2_HALF


def create_table_by_pil(filename):
    """Convert filename -> RGB data -> HTML table string using PIL.

    param[in]  filename: image file path.
    yield      created string '<table>...</table>'.
               ''.join(create_table(...)) is a good way to use output.
    """
    try:
        import PIL.Image
    except ImportError:
        print(PIL_IMPORT_ERROR, file=sys.stderr)
        raise
    with PIL.Image.open(filename) as src:
        width, height = src.size
        rgb_obj = src.getdata()
        yield from create_table(width, height, rgb_obj)


def create_canvas_by_pil(filename, canvas_id='canvas_id'):
    """Convert filename -> RGBA data -> HTML canvas string using PIL.

    param[in]  filename: image file path.
    param[in]  canvas_id: Id of canvas tag. in str.
    yield      created string '<canvas>...</canvas><script>...</script>'.
               ''.join(create_table(...)) is a good way to use output.
    """
    try:
        import PIL.Image
    except ImportError:
        print(PIL_IMPORT_ERROR, file=sys.stderr)
        raise
    with PIL.Image.open(filename) as src:
        width, height = src.size
        rgba_obj = src.getdata()
        has_alpha = src.mode == 'RGBA'
        yield from create_canvas(canvas_id, width, height, rgba_obj, has_alpha)


def main():
    """Call create_table_by_pil() or create_canvas_by_pil() via argparse.

    A simple interface to create HTML image string.
    If --id is set, then <canvas> image string is output.
    Else, <table> image string is output.

    $python html_image.py imagename --id canvas_id > sample.html
    is a good way to use this program.
    """
    # parse args using argparse
    import argparse
    parser = argparse.ArgumentParser(description=ARGPARSE_DESCRIPTION)
    parser.add_argument('-v', '--version', action='version',
                        version=('%(prog)s ' + __version__))
    parser.add_argument('file',
                        type=str, help='image file path')
    parser.add_argument('--id', metavar='id',
                        type=str, help='canvas id. mandatory for canvas')

    args = parser.parse_args()

    # call create_table_by_pil() or  create_canvas_by_pil(), and output
    print('<html><head></head><body>')
    if args.id:  # <canvas> mode. call create_canvas_by_pil()
        print(''.join(create_canvas_by_pil(args.file, args.id)))
    else:  # <table> mode. call create_table_by_pil()
        print(''.join(create_table_by_pil(args.file)))
    print('</body></html>')


if __name__ == '__main__':
    main()
