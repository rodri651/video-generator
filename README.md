# Video Generator
A combination of multiple libraries to generate a video, from multiple audio files and a fixed background music and single image

## Benefits of this Repo
Creates a video of the length of the speech audio file

Download all the audio files to one directory and just pass the path of this folder as an argument

Supports .mp3, .raw, .mp4, .webm, .ogg, .m4a audio files

Saves ALOT of time !!


## Usage
```
Clone this repo
pip install -r requirements.txt
```


Edit the generate\_videos.sh file with the audio-dir and output-dir arguments

Audio directory should contain the audio files that need to be converted to video
```
+ audio_nov_10
  - Malayalam.mp3
  - Mandarin.ogg
  - English.m4a
  ...
```
Run generate\_videos.sh, the videos will be created in the output directory 
```
+ output_audio_nov_4
  - Malyalam.mp4
  - Mandarin.mp4
  - English.mp4
  ...

```
