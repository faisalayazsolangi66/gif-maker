#!/usr/bin/env python3
"""Make an animated GIF from a folder of images.

Reads the images in a folder in filename order and stitches them
into one animated GIF. Frames are converted to a common size so the
animation does not jump around.
"""
import argparse
import os
import sys

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif"}


def collect_images(folder):
    return [os.path.join(folder, name) for name in sorted(os.listdir(folder))
            if os.path.isfile(os.path.join(folder, name))
            and os.path.splitext(name)[1].lower() in IMAGE_EXTS]


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Make an animated GIF from a folder of images."
    )
    parser.add_argument("input", help="folder containing the frames, in order")
    parser.add_argument("--output", default="animation.gif",
                        help="output GIF file (default: animation.gif)")
    parser.add_argument("--duration", type=int, default=500,
                        help="time per frame in milliseconds (default: 500)")
    parser.add_argument("--loop", type=int, default=0,
                        help="number of loops, 0 = forever (default: 0)")
    parser.add_argument("--width", type=int, default=0,
                        help="resize frames to this width (keeps aspect ratio, 0 = keep)")
    parser.add_argument("--height", type=int, default=0,
                        help="resize frames to this height (keeps aspect ratio, 0 = keep)")
    args = parser.parse_args(argv)

    if args.duration <= 0:
        parser.error("--duration must be positive")
    if args.loop < 0:
        parser.error("--loop must be 0 or more")

    try:
        from PIL import Image
    except ImportError:
        print("Error: Pillow is not installed. Install it with: pip install Pillow",
              file=sys.stderr)
        return 1

    if not os.path.isdir(args.input):
        print(f"Not a folder: {args.input}", file=sys.stderr)
        return 1

    files = collect_images(args.input)
    if len(files) < 2:
        print(f"Need at least 2 images in {args.input}, found {len(files)}.",
              file=sys.stderr)
        return 1

    frames = []
    try:
        for path in files:
            image = Image.open(path).convert("RGB")
            if args.width or args.height:
                width = args.width or int(image.width * args.height / image.height)
                height = args.height or int(image.height * args.width / image.width)
                image = image.resize((width, height))
            frames.append(image)
            print(f"Added frame: {path} ({image.width}x{image.height})")
    except Exception as exc:
        print(f"Failed to read a frame: {exc}", file=sys.stderr)
        return 1

    # Normalise all frames to the first frame's size.
    base_w, base_h = frames[0].size
    frames = [frame.resize((base_w, base_h)) if frame.size != (base_w, base_h)
              else frame for frame in frames]

    frames[0].save(args.output, save_all=True, append_images=frames[1:],
                   duration=args.duration, loop=args.loop, optimize=True)
    size_kb = os.path.getsize(args.output) / 1024
    print(f"Saved {args.output}: {len(frames)} frames, "
          f"{args.duration} ms each, {size_kb:.1f} KB.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
