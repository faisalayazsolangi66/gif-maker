# GIF Maker

Make an animated GIF from a folder of images. The images are used in filename order, so name your frames `01.png`, `02.png`, and so on. All frames are resized to the first frame's size so the animation does not jump around.

## Requirements

- Python 3
- Pillow (`pip install -r requirements.txt`)

## How to run

```bash
pip install -r requirements.txt
python3 main.py --help
python3 main.py frames/ --output animation.gif --duration 500
```

Options:

- `--output` — output GIF file (default: `animation.gif`)
- `--duration` — time per frame in milliseconds (default: `500`)
- `--loop` — number of loops, `0` = forever (default: `0`)
- `--width` / `--height` — resize frames (keeps aspect ratio, `0` = keep)

## Example

```bash
$ python3 main.py frames/ --output animation.gif --duration 300
Added frame: frames/01.png (400x300)
Added frame: frames/02.png (400x300)
Added frame: frames/03.png (400x300)
Saved animation.gif: 3 frames, 300 ms each, 42.1 KB.
```
