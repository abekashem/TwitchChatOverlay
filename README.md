# TwitchChatOverlay
Python code to convert a text log of Twitch chat to a video.

## Dependencies

Requires Python 3

```
pip install opencv-python
pip install pillow
pip install pandas
pip install numpy
pip install tqdm
```

## Example usage

```
python .\get_stream_video.py --log_path '../OverRustleLogsDownloader/logs/Jerma985 chatlog/' -o output.mp4 --index 192`
# --log_path location of all log .txt files
# -o output video name
# --index row of stream_data.csv for the target stream
```
