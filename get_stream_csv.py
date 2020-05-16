import argparse
import pandas as pd
from IPython.terminal.embed import InteractiveShellEmbed


def main():
    parser = argparse.ArgumentParser(
        description='Script to convert a text file of stream data to a csv.')
    parser.add_argument('-i', '--input', type=str, required=True,
                        help='Filepath of a .txt file with stream data.')
    parser.add_argument('-o', '--output', default='output.csv',
                        help='Output csv name.')
    args = parser.parse_args()

    with open(args.input, 'r') as f:
        text = f.read()

    words = text.split()

    months = [
        'Jan',
        'Feb',
        'Mar',
        'Apr',
        'May',
        'Jun',
        'Jul',
        'Aug',
        'Sep',
        'Oct',
        'Nov',
        'Dec',
    ]

    lines = []
    line = []

    for word in words:
        if word in months:
            if line:
                lines.append(' '.join(line))
            line = []
        line.append(word)

    rows = []
    for line in lines:
        words = line.split(' ')

        row = {
            'start_time': ' '.join(words[0: 4]),
            'duration': float(words[4]),
            'viewers': int(words[6].replace(',', '')),
            'views': int(words[7].replace(',', '')),
            'followers': int(words[8].replace(',', '')),
            'title': ' '.join(words[9:]),
        }
        rows.append(row)

    df = pd.DataFrame(rows)
    df['start_time'] = pd.to_datetime(df['start_time'],
                                      format='%b %d, %Y, %H:%M')
    df['end_time'] = df['start_time'] + pd.to_timedelta(df['duration'],
                                                        unit='hours')
    df.to_csv(args.output)


if __name__ == '__main__':
    main()
