<!--
 Copyright 2021 Nikhil Akki
 
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
 
     http://www.apache.org/licenses/LICENSE-2.0
 
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
-->

# A! in Audio Series 

Requirements -

- pipenv
- python 3.8+
- Tested with Linux/Unix like OS 
- GCP service account ([refer docs](https://cloud.google.com/speech-to-text/docs/quickstart-client-libraries))

_Note: - Google Cloud Platform (GCP) is a paid platform and a service account is required for this code work to work. This tutorial shouldn't cost any money (if used judiciously) since first 60 mins for GCP's STT service is free. [Refer the GCP's pricing section](https://cloud.google.com/speech-to-text/pricing) for exact details.

## How to run?
```
pipenv install # to install all dependencies
pipenv run python ui.py
```

### Sample url to test with -

1. gs://cloud-samples-data/speech/brooklyn_bridge.wav
1. gs://cloud-samples-data/speech/commercial_mono.wav
1. gs://cloud-samples-data/speech/commercial_stereo.wav
1. gs://cloud-samples-data/speech/corbeau_renard.flac
1. gs://cloud-samples-data/speech/en-US.wav
1. gs://cloud-samples-data/speech/hello.flac
1. gs://cloud-samples-data/speech/multi.wav
1. gs://cloud-samples-data/speech/multi_es.flac
1. gs://cloud-samples-data/speech/multi_es.wav
1. gs://cloud-samples-data/speech/time.mp3

___If you wish to test with your own audio files, make sure you create a GCS bucket and upload the file there (refer below links for detailed info)___

1. [GCloud SDK installation](https://cloud.google.com/sdk/docs/install)
1. [Create GCS Bucket](https://cloud.google.com/storage/docs/creating-buckets)
1. [Copy files from local to GCS bucket](https://cloud.google.com/storage/docs/gsutil/commands/cp)
