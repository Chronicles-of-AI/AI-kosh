# Copyright 2021 Team COA a.k.a Chronicles of AI
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Imports the Google Cloud client library
from google.cloud import speech


class GoogleSTT:
    def __init__(
        self, sample_rate_hertz: int = 16000, language_code: str = "en-US"
    ) -> None:

        # Instantiates a client
        self.client = speech.SpeechClient()
        self.sample_rate_hertz = sample_rate_hertz
        self.language_code = language_code

    def run_stt(self, gcs_uri: str):
        # The name of the audio file to transcribe
        self.audio = speech.RecognitionAudio(uri=gcs_uri)

        self.config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
            sample_rate_hertz=self.sample_rate_hertz,
            language_code=self.language_code,
        )

        # Detects speech in the audio file
        response = self.client.recognize(config=self.config, audio=self.audio)
        return response

    def get_transcript(self, response):
        transcript = [result.alternatives[0].transcript for result in response.results]
        return " ".join(transcript)

    def transcribe(self, gcs_uri: str):
        response = self.run_stt(gcs_uri)
        transcript = self.get_transcript(response)
        return transcript
