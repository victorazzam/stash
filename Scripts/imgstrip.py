import io, os, sys, glob, hashlib, warnings, argparse, multiprocessing
from PIL import Image

Image.LOAD_TRUNCATED_IMAGES = True

# PNG compression
# https://stackoverflow.com/a/71205362

# For HEIC support see:
# https://stackoverflow.com/a/69988418

use = 'imgstrip [options] <path> [path ...]'
desc = 'Remove unnecessary data from images to save space without sacrificing quality.'
end = 'Currently supports JPEG and PNG files.'
help_d = 'write to specific directory'
help_e = 'keep metadata'
help_i = 'include hidden files'
help_o = 'keep original file, append _min to original filename'
help_p = 'do not convert PNG to JPEG'
help_q = 'target quality, JPEG only, default: 75'
help_r = 'recursively traverse directories'
help_t = 'remove transparency, if present'
help_v = 'verbose mode'
parser = argparse.ArgumentParser(prog='imgstrip', usage=use, description=desc, epilog=end)
parser.add_argument('-d', dest='write', metavar='directory', help=help_d)
parser.add_argument('-e', '--exif', action='store_true', help=help_e)
parser.add_argument('-i', '--hidden', action='store_true', help=help_i)
parser.add_argument('-o', '--orig', action='store_true', help=help_o)
parser.add_argument('-p', '--png', action='store_true', help=help_p)
parser.add_argument('-q', dest='quality', metavar='[0-100]', type=int, choices=range(0, 101), default=75, help=help_q)
parser.add_argument('-r', '--recursive', action='store_true', help=help_r)
parser.add_argument('-t', '--transparency', action='store_true', help=help_t)
parser.add_argument('-v', '--verbose', action='store_true', help=help_v)
parser.add_argument('path', nargs='+', help='image or path to search for images')

def process(file, args):
    try:
        # Get image data
        img = Image.open(file)
        old = img.fp.read()
        img.fp.seek(0)

        # Check transparency
        transparent = img.mode == 'RGBA' and img.getextrema()[3][0] < 255 or 'transparency' in img.info
        mode = 'RGBA' if transparent and not args.transparency else 'RGB'

        # Set up new image
        new = io.BytesIO()
        name, ext = file.rsplit('.', 1)
        fmt = 'png' if args.png or mode == 'RGBA' else 'jpeg'

        # Ignore UserWarning about transparency caused by convert()
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')

            # Handle metadata, keep transparency if needed
            if not args.exif:
                for i in tuple(img.info):
                    if i == 'transparency' and mode == 'RGBA':
                        continue
                    del img.info[i]

            # Write new image
            img.convert(mode).save(new, format=fmt, optimize=True, quality=args.quality)
            img.close() # necessary for deletion later

        # Save if gains were made
        n, o = new.tell(), len(old)
        if n < o:

            # Keep or discard original
            if args.orig:
                name += '_min'
            else:
                os.remove(file)

            # Write to a specific directory
            if args.write:
                path, fname = os.path.split(name)
                name = args.write.rstrip('\\/') + os.sep + fname

            # Write as JPEG (.jpg) or PNG (.png)
            name += '.' + fmt.replace('e', '')
            with open(name, 'wb') as f:
                f.write(new.getvalue())

            # Calculate saved storage
            if args.verbose:
                percent = (o - n) / o * 100
                print('%s (%d) -> %s (%d) [reduced by %.2f%%]' % (file, o, name, n, percent))
        else:
            if args.verbose:
                print('Nothing to remove from ' + file)
    except Exception as e:
        log('Error: ' + file + ': ' + ', '.join(x for x in e.args if type(x) is str).lower())

def run(queue, args):
    for image in queue:
        process(image, args)

if __name__ == '__main__':
    try:
        args = parser.parse_args()

        if args.write:
            if os.path.isfile(args.write):
                sys.exit('Specified output path is not a directory.')
            elif not os.path.isdir(args.write):
                os.makedirs(args.write)

        exts = 'jpg jpeg png'.split()
        for f in args.path:
            if os.path.isdir(f):
                f = f.rstrip('\\/')

                search = ['/*.']
                if args.hidden:
                    search.append('/.*.')
                if args.recursive:
                    for s in search.copy():
                        search.append('/**' + s)

                queue = tuple(set(x for s in search for ext in exts for x in glob.iglob(f + s + ext, recursive=args.recursive)))
                procs = [multiprocessing.Process(target=run, args=(queue[x::8], args)) for x in range(0, 8)]
                [p.start() for p in procs]
                [p.join() for p in procs]
            else:
                process(f, args)
    except KeyboardInterrupt:
        print('\nInterrupted.')