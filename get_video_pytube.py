import os
import argparse
from tqdm import tqdm
from pytube import YouTube
from functools import partial
from tqdm import tqdm


def progress_function(chunk, file_handle, bytes_remaining, pbar):
    pbar.update(pbar.total - bytes_remaining - pbar.n)


def main():
    parser = argparse.ArgumentParser(
        description='Script to download a YouTube video.')
    parser.add_argument('--url', type=str, required=True,
                        help='Youtube video URL.')
    parser.add_argument('-o', '--output', default='output',
                        help='Output video name.')
    args = parser.parse_args()

    output_dir = os.path.dirname(args.output)
    output_name = os.path.basename(args.output)

    video_size = YouTube(args.url).streams.get_highest_resolution().filesize
    video = YouTube(
        args.url,
        on_progress_callback=partial(
            progress_function, pbar=tqdm(total=video_size)),
    ).streams.get_highest_resolution()

    print('Downloading video titled "{}" of resolution {} to {}/{}'
          .format(video.title, video.resolution, output_dir, output_name))

    video.download(output_path=output_dir, filename=output_name)


if __name__ == '__main__':
    main()
