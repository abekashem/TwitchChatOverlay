from pytube import YouTube
from functools import partial
from tqdm import tqdm


video_link = 'https://www.youtube.com/watch?v=cVW78lRj1a4'
output_name = 'pytube_output.mp4'


def progress_function(chunk, file_handle, bytes_remaining, pbar):
    pbar.update(pbar.total - bytes_remaining - pbar.n)


video_size = YouTube(video_link).streams.get_highest_resolution().filesize
video = YouTube(
    video_link,
    on_progress_callback=partial(
        progress_function, pbar=tqdm(total=video_size)),
).streams.get_highest_resolution()


print('Downloading video titled "{}" of resolution to {} as {}'
      .format(video.title, video.resolution, output_name))


video.download(filename=output_name,)
