import logging
import os
import subprocess

from dandere2x.dandere2xlib.utils.dandere2x_utils import get_a_valid_input_resolution
from dandere2x.dandere2xlib.utils.yaml_utils import get_options_from_section
from dandere2x.dandere2xlib.wrappers.ffmpeg.ffprobe import get_seconds
from dandere2x.dandere2xlib.wrappers.ffmpeg.videosettings import VideoSettings


def re_encode_video(ffmpeg_dir: str, ffprobe_dir: str, output_options: dict, input_file: str,
                    output_file: str, console_output=None):
    """
    #todo
    """

    if console_output:
        assert type(console_output) == str

    logger = logging.getLogger(__name__)
    video_settings = VideoSettings(ffprobe_dir=ffprobe_dir, video_file=input_file)
    frame_rate = video_settings.frame_rate

    extract_frames_command = [ffmpeg_dir,
                              "-i", input_file]

    extract_frames_options = \
        get_options_from_section(output_options["ffmpeg"]['pre_process_video']['output_options'],
                                 ffmpeg_command=True)

    for element in extract_frames_options:
        extract_frames_command.append(element)

    extract_frames_command.append("-r")
    extract_frames_command.append(str(frame_rate))
    extract_frames_command.extend([output_file])

    process = subprocess.Popen(extract_frames_command, stdout=open(os.devnull, 'w'), stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE, shell=False)

    stdout, stderr = process.communicate()


def convert_video_to_gif(ffmpeg_dir: str, input_path: str, output_path: str, output_options = None) -> None:
    assert os.path.exists(ffmpeg_dir), "% does not exist" % ffmpeg_dir

    execute = [
        ffmpeg_dir,
        "-i", input_path,
    ]

    options = get_options_from_section(output_options["ffmpeg"]['convert_video_to_gif']['output_options'],
                                       ffmpeg_command=True)

    for item in options:
        execute.append(item)

    execute.append(output_path)

    print(execute)
    process = subprocess.Popen(execute, stdout=open(os.devnull, 'w'), stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE, shell=False)

    stdout, stderr = process.communicate()


def convert_gif_to_video(ffmpeg_dir: str, input_path: str, output_path: str, output_options = None) -> None:
    assert os.path.exists(ffmpeg_dir), "% does not exist" % ffmpeg_dir

    execute = [
        ffmpeg_dir,
        "-i", input_path,
    ]

    options = get_options_from_section(output_options["ffmpeg"]['convert_video_to_gif']['output_options'],
                                       ffmpeg_command=True)

    for item in options:
        execute.append(item)

    execute.append(output_path)

    print(execute)
    process = subprocess.Popen(execute, stdout=open(os.devnull, 'w'), stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE, shell=False)

    stdout, stderr = process.communicate()



def check_if_file_is_video(ffprobe_dir: str, input_video: str):
    execute = [
        ffprobe_dir,
        "-i", input_video,
        "-v", "quiet"
    ]

    return_bytes = subprocess.run(execute, check=True, stdout=subprocess.PIPE).stdout

    if "Invalid data found when processing input" in return_bytes.decode("utf-8"):
        return False

    return True


def append_resize_filter_to_pre_process(output_options: dict, width: int, height: int, block_size: int):
    """
    < to do >
    """
    log = logging.getLogger()
    width, height = get_a_valid_input_resolution(width, height, block_size)

    log.info("Dandere2x is resizing the video in order to make the resolution compatible with your settings... ")
    log.info("New width -> %s " % str(width))
    log.info("New height -> %s " % str(height))

    output_options['ffmpeg']['pre_process_video']['output_options']['-vf'] \
        .append("scale=" + str(width) + ":" + str(height))


def append_dar_filter_to_pipe_process(output_options: dict, width: int, height: int) -> None:
    """
    < to do >
    """

    # reduce width and height down
    from fractions import Fraction
    frac = Fraction(width, height)
    frac_str = str(frac.numerator) + "/" + str(frac.denominator)

    output_options['ffmpeg']['pipe_video']['output_options']['-vf'].append("setdar=" + frac_str)


def divide_and_reencode_video(ffmpeg_dir: str, ffprobe_path: str,
                              input_video: str, output_options: dict,
                              divide: int, output_dir: str):
    """

    @param ffmpeg_dir:
    @param ffprobe_path:
    @param input_video:
    @param re_encode_settings:
    @param divide:
    @param output_dir:
    @return:
    """
    import math

    seconds = int(get_seconds(ffprobe_dir=ffprobe_path, input_video=input_video))
    ratio = math.ceil(seconds / divide)
    frame_rate = VideoSettings(ffprobe_dir=ffprobe_path, video_file=input_video).frame_rate

    execute = [ffmpeg_dir,
               "-i", input_video,
               "-f", "segment",
               "-segment_time", str(ratio),
               "-g", str(ratio),
               "-r", str(frame_rate),
               "-force_key_frames", "expr:gte(t,n_forced*%s)" % ratio,
               "-sc_threshold", "0"]

    print("execute %s" % str(execute))
    options = get_options_from_section(output_options["ffmpeg"]['pre_process_video']['output_options'],
                                       ffmpeg_command=True)

    for element in options:
        execute.append(element)

    execute.append(os.path.join(output_dir, "outputvid%d.mkv"))

    return_bytes = subprocess.run(execute, check=True, stdout=subprocess.PIPE).stdout
    return_string = return_bytes.decode("utf-8")

    return return_string


def get_console_output(method_name: str, console_output_dir=None):
    if console_output_dir:
        assert type(console_output_dir) == str

        log_file = os.path.join(console_output_dir, method_name + "output.txt")
        console_output = open(log_file, "w", encoding="utf8")
        return console_output

    return open(os.devnull, 'w')


def concat_n_videos(ffmpeg_dir: str, temp_file_dir: str, console_output_dir: str, list_of_files: list,
                    output_file: str) -> None:
    import subprocess

    file_list_text_file = os.path.join(temp_file_dir, "temp.txt")

    file_template = "file " + "'" + "%s" + "'" + "\n"

    # we need to create a text file for ffmpeg's concat function to work properly.
    file = open(file_list_text_file, "a")
    for file_name in list_of_files:
        file.write(file_template % file_name)
    file.close()

    concat_videos_command = [ffmpeg_dir,
                             "-f", "concat",
                             "-safe", "0",
                             "-i", file_list_text_file]

    concat_videos_command.extend([output_file])

    console_output = get_console_output(__name__, console_output_dir)
    subprocess.call(concat_videos_command, shell=False, stderr=console_output, stdout=console_output)


def migrate_tracks_contextless(ffmpeg_dir: str, no_audio: str, file_dir: str, output_file: str,
                               console_output_dir=None):
    """
    Add the audio tracks from the original video to the output video.
    """

    # to remove
    def convert(lst):
        return ' '.join(lst)

    log = logging.getLogger()

    migrate_tracks_command = [ffmpeg_dir,
                              "-i", no_audio,
                              "-i", file_dir,
                              "-map", "0:v?",
                              "-map", "1:a?",
                              "-map", "1:s?",
                              "-map", "1:d?",
                              "-map", "1:t?"
                              ]

    migrate_tracks_command.extend([str(output_file)])

    console_output = get_console_output(__name__, console_output_dir)

    log.info("Writing files to %s" % str(console_output_dir))
    log.info("Migrate Command: %s" % convert(migrate_tracks_command))
    subprocess.call(migrate_tracks_command, shell=False, stderr=console_output, stdout=console_output)
    log.info("Finished migrating to file: %s" % output_file)
