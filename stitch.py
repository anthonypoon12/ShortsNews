# Goal is to concatenate multiple mp4 files to a single file

import ffmpeg

# paths for mp4 files to be concatenated
input_files = []

# Output file name
output_file = 'output.mp4'

# Create a list of ffmpeg inputs for each file
input_streams = [ffmpeg.input(file) for file in input_files]

# Concatenate the input streams
joined = ffmpeg.concat(*input_streams, v=1, a=0)

# Output options
output_options = {
    # 'c:v': 'libx264',  # Use libx264 codec for video
    # 'crf': '20',       # Constant Rate Factor for quality (adjust as needed)
    # 'preset': 'slow',  # Preset for encoding speed (adjust as needed)
}

# Run ffmpeg to join the files
ffmpeg.output(joined, output_file, **output_options).run()
