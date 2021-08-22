from google.cloud import videointelligence_v1p3beta1 as videointelligence
import io

#
path = "/Users/arpitjain/Documents/POC/AI-kosh/video_intelligence/data/pets.mp4"

client = videointelligence.StreamingVideoIntelligenceServiceClient()

# Set streaming config.
config = videointelligence.StreamingVideoConfig(
    feature=(videointelligence.StreamingFeature.STREAMING_OBJECT_TRACKING)
)

# config_request should be the first in the stream of requests.
config_request = videointelligence.StreamingAnnotateVideoRequest(video_config=config)

# Set the chunk size to 5MB (recommended less than 10MB).
chunk_size = 5 * 1024 * 1024

# Load file content.
stream = []
with io.open(path, "rb") as video_file:
    while True:
        data = video_file.read(chunk_size)
        if not data:
            break
        stream.append(data)


def stream_generator():
    yield config_request
    for chunk in stream:
        yield videointelligence.StreamingAnnotateVideoRequest(input_content=chunk)


requests = stream_generator()

# streaming_annotate_video returns a generator.
# The default timeout is about 300 seconds.
# To process longer videos it should be set to
# larger than the length (in seconds) of the stream.
responses = client.streaming_annotate_video(requests, timeout=900)

# Each response corresponds to about 1 second of video.
for response in responses:
    # Check for errors.
    if response.error.message:
        print(response.error.message)
        break

    object_annotations = response.annotation_results.object_annotations

    # object_annotations could be empty
    if not object_annotations:
        continue

    for annotation in object_annotations:
        # Each annotation has one frame, which has a timeoffset.
        frame = annotation.frames[0]
        time_offset = frame.time_offset.seconds + frame.time_offset.microseconds / 1e6

        description = annotation.entity.description
        confidence = annotation.confidence

        # track_id tracks the same object in the video.
        track_id = annotation.track_id

        # description is in Unicode
        print("{}s".format(time_offset))
        print(u"\tEntity description: {}".format(description))
        print("\tTrack Id: {}".format(track_id))
        if annotation.entity.entity_id:
            print("\tEntity id: {}".format(annotation.entity.entity_id))

        print("\tConfidence: {}".format(confidence))

        # Every annotation has only one frame
        frame = annotation.frames[0]
        box = frame.normalized_bounding_box
        print("\tBounding box position:")
        print("\tleft  : {}".format(box.left))
        print("\ttop   : {}".format(box.top))
        print("\tright : {}".format(box.right))
        print("\tbottom: {}\n".format(box.bottom))
