"""Make the web copies of a profile photo (needs Pillow: pip install pillow).

    python profiles/_src/make_photo.py SOURCE.jpg SLUG [--crop LEFT TOP SIZE]

Writes profiles/SLUG/photo-<w>.webp for each width, plus photo-<w>.jpg for the
fallback width, all square, with no metadata (EXIF, GPS) copied from the source.
List the files in the person's content file under [photo].
"""
import argparse
from pathlib import Path

from PIL import Image, ImageOps

WIDTHS = [240, 480, 720]      # display size about 180-240 CSS px; 2x and 3x screens
FALLBACK = 480                # JPEG for browsers without WebP, and for link previews
PROFILES = Path(__file__).resolve().parent.parent


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("slug")
    ap.add_argument("--crop", nargs=3, type=int, metavar=("LEFT", "TOP", "SIZE"),
                    help="square crop in source pixels (default: centred square)")
    a = ap.parse_args()

    img = ImageOps.exif_transpose(Image.open(a.source)).convert("RGB")
    if a.crop:
        left, top, size = a.crop
    else:
        size = min(img.size)
        left, top = (img.width - size) // 2, (img.height - size) // 2
    img = img.crop((left, top, left + size, top + size))

    out_dir = PROFILES / a.slug
    out_dir.mkdir(parents=True, exist_ok=True)
    for w in WIDTHS:
        if w > size:
            continue
        small = img.resize((w, w), Image.Resampling.LANCZOS)
        webp = out_dir / f"photo-{w}.webp"
        small.save(webp, "WEBP", quality=80, method=6)
        print(f"wrote {webp.name}: {webp.stat().st_size / 1024:.0f} KB")
        if w == FALLBACK:
            jpg = out_dir / f"photo-{w}.jpg"
            small.save(jpg, "JPEG", quality=82, optimize=True, progressive=True)
            print(f"wrote {jpg.name}: {jpg.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
