import os
from google.cloud import texttospeech
from mutagen.mp3 import MP3
# import SummarySegment

content = "Good bye, world!"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="wired-column-412623-7844dfb99f80.json"
# Instantiates a client
client = texttospeech.TextToSpeechClient()

# Set the text input to be synthesized
synthesis_input = texttospeech.SynthesisInput(text=content)

# Build the voice request, select the language code ("en-US") and the ssml
# voice gender ("neutral")
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US", name="en-US-Journey-D"
)

# Select the type of audio file you want returned
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# Perform the text-to-speech request on the text input with the selected
# voice parameters and audio file type
response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

curr_len = 0
curr_audio = None
# The response's audio_content is binary.
with open("output.mp3", "wb") as out:
    # Write the response to the output file.
    out.write(response.audio_content)
    print('Audio content written to file "output.mp3"')
    curr_audio = MP3("output.mp3")
    curr_len = curr_audio.info.length
    print(curr_len)

