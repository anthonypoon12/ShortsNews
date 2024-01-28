import ffmpeg

def merge(videofile, audiofile, outputfile):
    input_video = ffmpeg.input(videofile)
    input_audio = ffmpeg.input(audiofile)
    ffmpeg.concat(input_video, input_audio, v=1, a=1).output(outputfile).run()

if __name__ == '__main__':
    import sys
    merge(sys.argv[1], sys.argv[2], sys.argv[3])