import os
import argparse
import pandas as pd
from get_video import logs_to_df, df_to_video
from IPython.terminal.embed import InteractiveShellEmbed


def get_path_df(log_path) -> pd.DataFrame:
    """
    Get a dataframe with a column of file paths, and a column of dates.
    """
    paths = []
    dates = []

    for root, dirs, files in os.walk(log_path):
        for f in files:
            if f.endswith('.txt') and f[0] == '2':
                paths.append(os.path.join(root, f))
                dates.append(f[:-4])

    df = pd.DataFrame({'path': paths, 'date': dates})
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    return df


def main():
    parser = argparse.ArgumentParser(
        description='Script to convert a text file of stream data to a csv.')
    parser.add_argument('--log_path', type=str, required=True,
                        help='Filepath containing .txt logs.')
    parser.add_argument('--stream_csv', type=str, default='stream_data.csv',
                        help='Filepath of a .csv file with stream data.')
    parser.add_argument('-o', '--output', default='output.mp4',
                        help='Output video name.')
    parser.add_argument('--index', type=int, required=True,
                        help='Index of stream CSV to get video for.')
    args = parser.parse_args()

    stream_df = pd.read_csv(args.stream_csv,
                            parse_dates=['start_time', 'end_time'])
    path_df = get_path_df(args.log_path)

    path_df.sort_values('date')

    stream = stream_df.iloc[192]
    start_time = stream['start_time']
    end_time = stream['end_time']

    # Get relevant logs in case streams go through midnight
    relevant_logs = path_df[
        (path_df['date'] >= start_time.floor('D')) &
        (path_df['date'] <= end_time.ceil('D'))
    ]

    # Concatenate neighboring logs into one dataframe
    logs_df = pd.concat([logs_to_df(path) for path in relevant_logs['path']])

    # Query the logs by stream start and end
    logs_df = logs_df[
        (logs_df['date'] >= start_time) & (logs_df['date'] <= end_time)
    ]

    df_to_video(logs_df, video_name=args.output)


if __name__ == '__main__':
    main()
