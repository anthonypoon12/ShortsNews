# Goal is to concatenate multiple mp4 files to a single file

import ffmpeg

def stitch(input_files):
    output_file = 'output.mp4'

    # Create a list of ffmpeg inputs for each file
    input_streams = []

    for file in input_files:
        input_streams.append(ffmpeg.input(file))

    # Force all inputs to have the same resolution and aspect ratio
    input_streams = [inp.filter('scale', size='480x268').filter('setsar', ratio='1:1') for inp in input_streams]


    # Concatenate the input streams
    joined = ffmpeg.concat(*input_streams, v=1, a=0)

    # Output options
    output_options = {
        'c:v': 'libx264',  # Use libx264 codec for video
        'crf': '20',       # Constant Rate Factor for quality (adjust as needed)
        'preset': 'slow',  # Preset for encoding speed (adjust as needed)
    }

    # Run ffmpeg to join the files
    ffmpeg.output(joined, output_file, **output_options).run()


if __name__ == "__main__":
    import sys
    stitch(*sys.argv[1:])

    import ffmpeg