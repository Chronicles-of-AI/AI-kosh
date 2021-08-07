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

from magicgui import magicgui
from stt import GoogleSTT


# decorate your function with the @magicgui decorator
@magicgui(call_button="Transcribe", result_widget=True)
def transcribe(uri: str):
    try:
        gstt = GoogleSTT(sample_rate_hertz=44100)
        transcript = gstt.transcribe(uri)
        print(f"{transcript=}")
        return transcript
    except Exception as error:
        return error


# your function is now capable of showing a GUI
transcribe.show(run=True)
