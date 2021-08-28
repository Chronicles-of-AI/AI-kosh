from pytube import YouTube
import os
import pandas as pd

path = "/Users/arpitjain/Documents/POC/AI-kosh/video_intelligence/video_automl/annotations/human_action_dataset.csv"

static_url = "https://www.youtube.com/watch?v="
gcs_bucket_uri = "gs://coa_video_ai_automl/"


def downloadYouTube(videourl, path):

    try:
        yt = YouTube(videourl)
        yt = (
            yt.streams.filter(progressive=True, file_extension="mp4")
            .order_by("resolution")
            .desc()
            .last()
        )
        if not os.path.exists(path):
            os.makedirs(path)
        file_name = yt.get_file_path().split("/")[-1]
        if os.path.exists(os.path.join(path, file_name)):
            return file_name
        yt.download(path)
        return file_name
    except:
        return None


def read_csv(path: str):
    gcs_uri_list = []
    label_list = []
    start_time_list = []
    end_time_list = []
    df = pd.read_csv(path)
    for row in df.iterrows():
        video_id = row[1][1]
        youtube_url = f"{static_url}{video_id}"
        local_video_name = downloadYouTube(
            videourl=youtube_url,
            path="/Users/arpitjain/Documents/POC/AI-kosh/video_intelligence/video_automl/data",
        )
        print(f"Downloading video: {local_video_name}")
        if local_video_name is not None:
            gcs_video_path = f"{gcs_bucket_uri}{local_video_name}"
            gcs_uri_list.append(gcs_video_path)
            label_list.append(row[1][0])
            start_time_list.append(row[1][2])
            end_time_list.append(row[1][3])
        else:
            continue
    master_data = {
        "uri": gcs_uri_list,
        "label": label_list,
        "start_time": start_time_list,
        "end_time": end_time_list,
    }
    temp_df = pd.DataFrame(master_data)
    temp_df.to_csv(
        "/Users/arpitjain/Documents/POC/AI-kosh/video_intelligence/video_automl/annotations/annotation.csv"
    )


read_csv(path=path)
