import ffmpeg
from pathlib import Path
import argparse
from datetime import datetime
from pandas import DataFrame
import math
from tqdm import tqdm

def main(input_folder: Path):

    duration_sec_list = []

    filenames = list(input_folder.glob("*"))
    for fn in tqdm(filenames):
        if fn.is_dir():
            continue
        try:
            meta = ffmpeg.probe(fn)
        except Exception as e:
            print(f"some error with {fn}, skip")
            continue

        duration_sec = meta['format']['duration']
        duration_sec_list.append(float(duration_sec))

    df = DataFrame({"filename": [fn.name for fn in filenames], "dur_sec": duration_sec_list})
    df.sort_values(by="dur_sec", inplace=True, ascending=False)
    df.reset_index(inplace=True, drop=True)

    print(f"There are {len(filenames)} video files.")

    print(df.head())
    print(df.tail())

    dur_sum_sec = df["dur_sec"].sum()
    dur_sum_min = dur_sum_sec / 60.0
    dur_sum_h = dur_sum_min / 60.0

    dur_sum_h_floor = math.floor(dur_sum_h)
    dur_sum_min_remainder = int(dur_sum_min - 60*dur_sum_h_floor)

    print(f"total duration: {dur_sum_h_floor}h {dur_sum_min_remainder}min")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", type=Path, default="/home/david/Videos/from_google_photos")
    args = parser.parse_args()

    input_folder = args.input

    main(input_folder)
