"""
Convert To WAV

This script converts all audio files in the specified directory (or current directory if none is specified) to WAV format using ffmpeg.
The converted files are saved in a 'converted' folder within the specified directory, preserving the original directory structure.


Sample rate: 44100 Hz   (CD quality)
Bit depth: 16-bit       (WAV is uncompressed, the bit depth is set to 16-bit for compatibility)
Mono channel: 1 channel (for voice recordings, mono is often sufficient and reduces file size)
"""

__author__ = "Mefamex"
__created__ = "2026-08-04"
__updated__ = "2026-08-04"
__url_github__ = "https://github.com/Mefamex/python-code-snippets"

import subprocess
from pathlib import Path

def convert_all_to_wav(pathh:str = ""):
    if not Path.is_dir(Path(pathh)) and pathh != "":
        print(f"❌ error: '{pathh}' is not a valid directory. Please provide a valid path or leave it empty to use the current directory.")
        return
    base_dir = Path(pathh) if Path.is_dir(Path(pathh)) else Path.cwd()
    output_dir = base_dir / "converted"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    audio_files = []
    for path in base_dir.rglob("*.*"):
        if "converted" not in path.parts and path.suffix.lower() in [".mp3", ".ogg", ".flac"]:
            audio_files.append(path)
    print(f" {len(audio_files)} audio files found. Conversion starting...\n")
    
    for count, audio_path in enumerate(audio_files, 1):
        relative_path = audio_path.relative_to(base_dir)
        wav_path = output_dir / relative_path.with_suffix('.wav')
        wav_path.parent.mkdir(parents=True, exist_ok=True)
        command = [ "ffmpeg", "-y", "-i", str(audio_path), "-ac", "1", "-ar", "44100", "-sample_fmt", "s16", str(wav_path) ]
        try:
            # run with stdout and stderr redirected to DEVNULL to suppress output
            subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            print(f"[{count}/{len(audio_files)}] ✅ {relative_path.parent.name}/{wav_path.name}")
        except subprocess.CalledProcessError: print(f"[{count}/{len(audio_files)}] ❌ Error occurred: {relative_path}")
    print("\n🎉 All conversion processes completed! Audio files are ready in the 'converted' folder.")

if __name__ == "__main__":
    # Check if ffmpeg is installed
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        convert_all_to_wav()
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Error: 'ffmpeg' not found in the system. Please install it: sudo pacman -S ffmpeg")
