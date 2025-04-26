import ffmpeg
from pathlib import Path
import argparse
from datetime import datetime

def filename_starts_with_date(fn: Path):
    name = fn.name

    try:
        datetime(year=int(name[:4]), month=int(name[4:6]), day=int(name[6:8]))
        return True
    except Exception as e:
        return False

def main(input_folder: Path, is_dry: bool = True):
    if is_dry:
        print("dry run\n\n")

    filenames = list(input_folder.glob("*"))
    for fn in filenames:
        if fn.is_dir():
            continue
        try:
            meta = ffmpeg.probe(fn)
        except Exception as e:
            print(f"some error with {fn}, skip")
            continue
        if not filename_starts_with_date(fn):
            creation_time = meta["format"]["tags"]["creation_time"]
            year, month, day = creation_time[:4], creation_time[5:7], creation_time[8:10]
            new_filename = fn.parent / f"{year}{month}{day}_{fn.name}"
            if is_dry:
                print(f"{fn} -> {new_filename}")
            else:
                fn.rename(new_filename)
        else:
            if is_dry:
                print(f"{fn} unchanged.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", type=Path, default="/home/david/Videos/from_google_photos")
    parser.add_argument("--dry", "-n", action="store_true")
    args = parser.parse_args()

    input_folder = args.input
    is_dry = args.dry

    main(input_folder, is_dry)
