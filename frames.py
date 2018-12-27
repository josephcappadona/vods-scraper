import sys, os, subprocess

args = sys.argv
if len(args) < 2:
    print('USAGE:  python frames.py VIDEO_FILEPATH [FFMPEG_ARGS ...]')
    exit()
video_filepath = args[1]
ffmpeg_args = ' '.join(args[2:])

video_filename = video_filepath.split('/')[-1]
video_name = video_filename[:video_filename.rfind('.')]
print('\n\nDownloading %s\n' %video_name)

data_dir = "./data"
frames_dir = "%s/%s" % (data_dir, video_name)
#print(frames_dir)
os.makedirs(frames_dir, exist_ok=True)

ffmpeg_command = "ffmpeg -i \"{}\" {} \"{}/image-%06d.png\" -hide_banner".format(video_filepath, ffmpeg_args, frames_dir)
print('\nLogging ffmpeg command in %s' % ffmpeg_command)
#subprocess.run("echo %s > %s" % (ffmpeg_command, '%s/command' % frames_dir), shell=True, check=True)
command_filepath = frames_dir + '/command'
with open(command_filepath, 'w+') as command_file:
    command_file.write(ffmpeg_command)
subprocess.run("eval `cat \"%s\"`" % command_filepath, shell=True, check=True)
print('\n\nFrames written to %s\n' % frames_dir)
