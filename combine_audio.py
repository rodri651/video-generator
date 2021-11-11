"""
Assumes the audio file is shorter than the backround music file
"""


import argparse
from os import listdir, mkdir, remove
from os.path import isfile, join, isdir, split

from termcolor import colored
from pydub import AudioSegment
import ffmpeg
from moviepy.editor import AudioFileClip, ImageClip

def generate_file_list(dir_path):
    onlyfiles = [join(dir_path,f) for f in listdir(dir_path) if isfile(join(dir_path, f))]
    return onlyfiles

def check_files(opt):
    if not isfile(opt.background_audio):
        print(colored("[DEBUG] Background audio file does not exist: %s", 'red')%(opt.background_audio))
        exit(0)

    if not isfile(opt.background_img):
        print(colored("[DEBUG] Background image file does not exist: %s", 'red')%(opt.background_img))
        exit(0)

    if not isdir(opt.audio_dir):
        print(colored("[DEBUG] Audio Directory does not exist: %s", 'red')%(opt.audio_dir))
        exit(0)

    if not isdir(opt.output_dir):
        mkdir(opt.output_dir)


def add_static_image_to_audio(image_path, audio_path, output_path):
    """Create and save a video file to `output_path` after 
    combining a static image that is located in `image_path` 
    with an audio file in `audio_path`"""
    audio_clip = AudioFileClip(audio_path)
    remove(audio_path)
    image_clip = ImageClip(image_path)
    video_clip = image_clip.set_audio(audio_clip)
    video_clip.duration = audio_clip.duration
    video_clip.fps = 1
    video_clip.write_videofile(output_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--audio-dir', type=str, default='Nov2_audio/', help='Directory with voice recordings')
    parser.add_argument('--background-audio', type=str, default='background_music.mp3', help='Background audio file')
    parser.add_argument('--output-dir', type=str, default='output_Nov2/', help='Output directory')
    parser.add_argument('--background_img', type=str, default='background_image.jpeg', help='Background Image')
    
    opt = parser.parse_args()

    print(opt, "\n\n \N{rocket} \N{rocket} \N{rocket}")
    check_files(opt)

    background_audio = AudioSegment.from_file(opt.background_audio, opt.background_audio.split('.')[-1])
    background_audio = background_audio - 20

    

    audio_files = generate_file_list(opt.audio_dir)
    
    for i,file_name in enumerate(audio_files):
        
        file_format = file_name.split('.')[-1]

        if file_format=='mpga':
            new_file_name = file_name.split('.')[0]+'.mp3'
            ffmpeg.input(file_name).output(new_file_name).run(overwrite_output=True)
            file_name=new_file_name
            file_format='mp3'

        
        if file_format in ['mp3','raw','mp4','webm','ogg','m4a']:
            output_file = join(opt.output_dir,split(file_name)[-1])
            print("[DEBUG] [%d] Processing : %s" %(i,file_name) )
            speech = AudioSegment.from_file(file_name, file_format)
            if not (speech.max_dBFS - background_audio.dBFS)>20:
                print("Increased volume")
                speech += 20 - (speech.max_dBFS - background_audio.dBFS) 
            mix_audio = speech.overlay(background_audio[:len(speech)])
            mix_audio.export(output_file, format="mp3")
            add_static_image_to_audio(opt.background_img, output_file, output_file.split('.')[0]+'.mp4')

        
        else:
            print(colored("[DEBUG] [%d] Unable to parse audio: %s",'red')%(i,file_name))

    print(colored("Praise Jesus !!! Jump Shout and Celebrate this Day: You just saved %d minutes \N{party popper} \N{smiling face with sunglasses}  \n\n", 'green', attrs=['bold'])%(10*len(audio_files)))