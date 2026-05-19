"""
Instagram için görsel optimizasyonu.
- Girdi klasoru: convert
- Cikti klasoru: converted

requirements.txt:
Pillow
pillow-heif
rawpy

"""

from __future__ import annotations

import io, sys
from pathlib import Path
from typing import Iterable, Tuple

from PIL import Image, ImageCms, ImageFilter

# RAW destegi icin istege bagli kutuphane
try:
    import rawpy
    RAW_AVAILABLE = True
except Exception:
    RAW_AVAILABLE = False

# HEIC/HEIF destegi icin istege bagli kutuphane
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
    HEIF_AVAILABLE = True
except Exception: HEIF_AVAILABLE = False


RAW_EXTS = {".arw"}
SUPPORTED_EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".webp", ".heic", ".heif"} | RAW_EXTS


def ask_output_format() -> Tuple[int, int]:
    """Kullanicidan hedef Instagram formatini alir ve boyut dondurur."""
    print("Hangi Instagram formatini istiyorsunuz?")
    print("1) Dikey   4:5  1080x1350")
    print("2) Kare    1:1  1080x1080")
    print("3) Yatay 1.91:1 1080x566")
    print("4) Reels   9:16 1080x1920")

    choice = input("Seciminiz (1/2/3/4) [varsayilan: 1]: ").strip()
    if not choice: choice = "1"
    if choice == "1": return (2160, 2700)
    if choice == "2": return (2160, 2160)
    if choice == "3": return (2160, 1131)
    if choice == "4": return (2160, 3840)

    print("Gecersiz secim.")
    return ask_output_format()


def ask_background_mode() -> str:
    """Kullanicidan arka plan modunu alir."""
    print("Arka plan tercihi nedir?")
    print("1) Siyah")
    print("2) Beyaz")
    print("3) Blur")

    choice = input("Seciminiz (1/2/3) [varsayilan: 1]: ").strip()
    if not choice: choice = "1"
    if choice == "1": return "black"
    if choice == "2": return "white"
    if choice == "3": return "blur"

    print("Gecersiz secim.")
    return ask_background_mode()


def iter_images(folder: Path) -> Iterable[Path]:
    """Desteklenen uzantilara sahip dosyalari listeler."""
    for path in sorted(folder.iterdir()):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTS:
            yield path


def load_input_image(path: Path) -> Image.Image:
    """Girdiyi PIL Image olarak yukler (RAW dahil)."""
    if path.suffix.lower() in RAW_EXTS:
        if not RAW_AVAILABLE:
            raise RuntimeError("RAW icin 'rawpy' kurulu degil")
        with rawpy.imread(str(path)) as raw:
            rgb = raw.postprocess(use_camera_wb=True, output_bps=8)
        return Image.fromarray(rgb)

    with Image.open(path) as img:
        return img.copy()


def convert_to_srgb(img: Image.Image) -> Image.Image:
    """Gorseli sRGB renk uzayina cevirir."""
    # ICC profili varsa, profileToProfile ile donusum yapilir.
    icc_bytes = img.info.get("icc_profile")
    if icc_bytes:
        try:
            src_profile = ImageCms.ImageCmsProfile(io.BytesIO(icc_bytes))
            dst_profile = ImageCms.createProfile("sRGB")
            return ImageCms.profileToProfile(img, src_profile, dst_profile, outputMode="RGB")
        except Exception: pass

    # ICC yoksa (veya hata varsa) RGB'ye zorla.
    if img.mode != "RGB": return img.convert("RGB")
    return img


def ensure_rgb_no_alpha(img: Image.Image) -> Image.Image:
    """JPEG kaydi icin alfa kanali varsa beyaz zemine birlestirir."""
    if img.mode in {"RGBA", "LA"}:
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[-1])
        return background
    if img.mode != "RGB": return img.convert("RGB")
    return img


def fit_with_background(img: Image.Image, target_w: int, target_h: int, mode: str) -> Image.Image:
    """Orani bozmadan sigdir ve arka planla tamamla."""
    src_w, src_h = img.size
    scale = min(target_w / src_w, target_h / src_h)
    new_w = int(round(src_w * scale))
    new_h = int(round(src_h * scale))

    resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    if mode == "white":
        canvas = Image.new("RGB", (target_w, target_h), (255, 255, 255))
    elif mode == "blur":
        base = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        canvas = base.filter(ImageFilter.GaussianBlur(radius=32))
    else:
        canvas = Image.new("RGB", (target_w, target_h), (0, 0, 0))
    left = (target_w - new_w) // 2
    top = (target_h - new_h) // 2
    canvas.paste(resized, (left, top))
    return canvas


def save_jpeg_under_limit(img: Image.Image, out_path: Path, max_bytes: int = 8 * 1024 * 1024) -> None:
    """JPEG olarak kaydeder; 8MB uzerindeyse kaliteyi dusurur."""
    quality = 100
    min_quality = 60

    while True:
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=quality, optimize=True)
        size = buffer.tell()

        if size <= max_bytes or quality <= min_quality:
            out_path.write_bytes(buffer.getvalue())
            return

        # Boyut fazla ise kaliteyi kademeli dusur.
        quality -= 5


def main() -> None:
    target_w, target_h = ask_output_format()
    bg_mode = ask_background_mode()

    base_dir = Path(__file__).resolve().parent
    input_dir = base_dir / "convert"
    output_dir = base_dir / "converted"

    # Klasorler yoksa olustur.
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not HEIF_AVAILABLE:
        print("Not: HEIC/HEIF icin 'pillow-heif' kurulu degil, bu dosyalar atlanacak.")
    if not RAW_AVAILABLE:
        print("Not: RAW (ARW) icin 'rawpy' kurulu degil, bu dosyalar atlanacak.")

    images = list(iter_images(input_dir))
    if not images:
        print(f"Islenecek gorsel bulunamadi: {input_dir}")
        return

    total = len(images)
    for idx, path in enumerate(images, start=1):
        if path.suffix.lower() in {".heic", ".heif"} and not HEIF_AVAILABLE:
            print(f"{idx}/{total} atlandi (HEIC destegi yok): {path.name}")
            continue
        if path.suffix.lower() in RAW_EXTS and not RAW_AVAILABLE:
            print(f"{idx}/{total} atlandi (RAW destegi yok): {path.name}")
            continue
        try:
            img = load_input_image(path)
            # Renk uzayini sRGB'ye donustur.
            img = convert_to_srgb(img)
            # JPEG icin alfa kanali temizle.
            img = ensure_rgb_no_alpha(img)
            # Orani bozmadan sigdir ve arka planla tamamla.
            img = fit_with_background(img, target_w, target_h, bg_mode)

            out_name = path.stem + ".jpg"
            out_path = output_dir / out_name
            save_jpeg_under_limit(img, out_path)

            print(f"{idx}/{total} islendi: {path.name}")
        except Exception as exc:
            print(f"{idx}/{total} atlandi (hata): {path.name} -> {exc}")


if __name__ == "__main__":
    main()
