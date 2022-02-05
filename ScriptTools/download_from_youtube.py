import sys
import click
from pytube import YouTube
from pathlib import Path
'''
RESOURCES:
    1. https://github.com/pytube/pytube
        - Original pytube repo.
    2. https://pytube.io/en/latest/
        - Pytube documentation website.
    3. https://stackoverflow.com/questions/70060263/pytube-attributeerror-nonetype-object-has-no-attribute-span
        - Stackoverflow post describing the exact error I was experiencing.
    4. https://github.com/baxterisme/pytube
        - Fork needed to make program work. Has needed regex fix in pytube/parser.py (on line 152 in v11.0.1).
'''


def read_video_list(filename, delimiter):
    f = open(filename,'r')
    content = f.read()
    print(content)
    if(delimiter != None):
        content = content.split(delimiter)
    else:
        content = content.split()
    print(content)
    f.close()
    return content

def download_from_youtube(urls, save_path, audio_only=False, save_captions=False, interactive_mode=False):
    def interactively_select_itag(stream_options):
        for option in stream_options:
            print(option)
        itag_choice = input("Please select your stream option by the 'itag' number:\t")
        return itag_choice
    
    def download_stream_by_itag(yt, itag_choice, filename_override=None):
        try:
            stream = yt.streams.get_by_itag(int(itag_choice))
        except Exception as e:
            print(f"Error with the itag that was selected: {itag_choice}")
            print(e)
        else:
            # No exception when selecting itag
            try:
                stream.download(output_path=save_path)
            except Exception as e:
                print(f"Error when trying to download the following: {yt.title}")
                print(e)

        

    def download_captions(video_title, captions):
        caption_file = open(video_title, 'w')
        caption_file.write(captions.generate_srt_captions())
        caption_file.close()

    for url in urls:
        yt = YouTube(url)
        print(yt)    
        if(audio_only):
            audio_stream_options = yt.streams.filter(only_audio=True)
            if(interactive_mode):
                itag_choice = interactively_select_itag(audio_stream_options)
        else:
            video_stream_options = yt.streams.filter(file_extension='mp4')
            if(interactive_mode):
                itag_choice = interactively_select_itag(video_stream_options)

        download_stream_by_itag(yt, itag_choice)

        if(save_captions):
            write_captions_file = True
            if('en' in yt.captions.keys()):
                # Priotize American English if it is available.
                captions = yt.captions.get_by_language_code('en')
            elif('en-GB' in yt.captions.keys()):
                # Check to see if we can use British English if American English is not available
                captions = yt.captions.get_by_language_code('en-GB')
            else:
                print("No English Captions Available")
                write_captions_file = False
            if(write_captions_file):
                download_captions(yt.title, captions)


@click.command()
@click.option('--video-list', 'video_list_filename', type=str, default=None, required=False)
@click.option('--list-delimiter', 'list_delimiter', type=str, default=None, required=False)
@click.option('--url', 'url', type=str, default=None, required=False)
@click.option('--audio-only', 'audio_only', is_flag=True, default=False)
@click.option('--save-captions', 'save_captions', is_flag=True, default=False)
@click.option('--interactive', 'interactive_mode', is_flag=True, default=False)
@click.option('--save-path', 'save_path', type=str, default=(Path.home()/"Downloads"), required=False)
def main(
        video_list_filename,
        list_delimiter,url,
        audio_only,
        save_captions,
        interactive_mode,
        save_path
        ):
    urls = []
    if(video_list_filename != None):
        urls.extend( read_video_list(video_list_filename, list_delimiter) )
    if(url != None):
        print(url)
        urls.append(url)
    print(urls)
    download_from_youtube(urls, save_path, audio_only=audio_only, save_captions=save_captions, interactive_mode=interactive_mode)
    print("ALL DONE")
    return 0


if __name__ == "__main__":
    main()
