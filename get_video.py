import os
import cv2
from PIL import (
    Image,
    ImageDraw,
    ImageFont,
)
import argparse
import textwrap
import numpy as np
import pandas as pd
from tqdm import tqdm
from typing import Tuple, List
from IPython.terminal.embed import InteractiveShellEmbed


def logs_to_df(log_path: str, date_end_idx: int = 20) -> pd.DataFrame:
    """
    Take an Overrustle .txt log and turn it into a pandas dataframe
    with columns for date, username, and message.
    """
    rows = []
    with open(log_path, 'r', encoding='utf8') as reader:
        line = reader.readline()
        while line != '':
            line = reader.readline()

            date = line[1: date_end_idx]

            # Get username based on the index of the colon : after the date
            username_end_idx = date_end_idx + line[date_end_idx:].find(':')
            username = line[date_end_idx + 6: username_end_idx]
            # Add a colon to the username for convenience
            username = '{}:'.format(username)

            message = line[username_end_idx + 1: -1]

            if not all([date, username, message]):
                continue

            rows.append({
                'date': date,
                'username': username,
                'message': message,
            })

    df = pd.DataFrame(rows)
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M:%S')
    return df


def wrap_messages(username_text: List[str],
                  message_text: List[str],
                  max_text_width: int = 30,
                  indent_width: int = 4) -> str:
    """
    Get a single string of chat messages with line breaks,
    with long messages wrapped into new lines.
    """
    lines = []
    for usr, msg in zip(username_text, message_text):
        wrapped_msg = textwrap.wrap(msg, width=max_text_width)
        wrapped_msg = ('\n' + ' '*indent_width).join(wrapped_msg)
        line = '{} {}'.format(usr, wrapped_msg)
        lines.append(line)
    return '\n'.join(lines)


def df_to_image(df: pd.DataFrame,
                image_size: Tuple[int, int] = (350, 1080),
                text_position: Tuple[int, int] = (5, 5),
                font_size: int = 18,
                text_color: Tuple[int, int, int] = (215, 215, 215),
                bg_color: Tuple[int, int, int] = (25, 25, 25)) -> Image:
    """
    Take a log dataframe and overlay its text on a blank image.
    """
    image = Image.new('RGB', image_size, color=bg_color)
    message_text = df['message'].values.tolist()
    username_text = df['username'].values.tolist()

    # Get each line of text as username: message
    text_for_image = wrap_messages(username_text, message_text)

    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(
        font=r'C:\Users\System-Pc\Desktop\arial.ttf',
        size=font_size,
    )
    draw.text(
        xy=text_position,
        text=text_for_image,
        font=font,
        align='left',
        fill=text_color,
    )
    return image


def fill_df(df: pd.DataFrame,
            stored_df: pd.DataFrame,
            target_len: int = 50) -> pd.DataFrame:
    """
    Place rows from the stored dataframe before the target
    dataframe in order to reach the target number of rows.
    """
    rows_from_stored = target_len - len(df.index)

    if rows_from_stored <= 0:
        # If the rows are negative, the target dataframe already has
        # enough rows, so just get the target rows from the bottom
        return df.tail(target_len)
    else:
        # Otherwise, take the needed rows from the stored dataframe
        return pd.concat([stored_df.tail(rows_from_stored), df])


def df_to_video(df: pd.DataFrame,
                video_name: str,
                video_size: Tuple[int, int] = (400, 1080),
                max_messages: int = 50):
    """
    Write a video of chat based on an Overrustle log .txt file
    """
    frames_per_second = 1

    # Initialize an OpenCV VideoWriter to create an mp4
    video_writer = cv2.VideoWriter(
        video_name,
        cv2.VideoWriter_fourcc(*'mp4v'),
        frames_per_second,
        video_size,
    )

    # Make a dataframe that's empty to use to fill in for
    # a dataframe that doesn't have enough rows
    df_for_image = pd.DataFrame([{
        'date': '',
        'username': '',
        'message': '',
    }]*max_messages)
    # Get a list of dates for every second
    # between the first and last date
    min_date, max_date = df['date'].min(), df['date'].max()
    duration = int((max_date - min_date).total_seconds())
    dates = [
        min_date + pd.Timedelta(seconds=second)
        for second in range(duration)
    ]
    # Loop through each second
    for date in tqdm(dates):
        if not date:
            continue

        date_df = df[df['date'] == date]
        df_for_image = fill_df(
            df=date_df,
            stored_df=df_for_image,
            target_len=max_messages,
        ).copy()

        image = df_to_image(
            df=df_for_image,
            image_size=video_size,
            text_position=(5, 5),
        )
        # Convert image to an OpenCV acceptable numpy array and write to video
        video_writer.write(np.array(image))
    video_writer.release()


def main():
    """
    Write a video based on an Overrustle chat log.
    """
    parser = argparse.ArgumentParser(
        description='Script to convert an Overrustle log to a chat video.')
    parser.add_argument('-i', '--input', type=str,
                        default='OverRustleLogsDownloader/logs/Jerma985 chatlog/December 2019/2019-12-29.txt',
                        help='Filepath of an overrustle log file (.txt)')
    parser.add_argument('-o', '--output', default='output.mp4',
                        help='Output video name, ')
    args = parser.parse_args()

    df = logs_to_df(args.input)
    df_to_video(df=df, video_name=args.output)


if __name__ == '__main__':
    main()
