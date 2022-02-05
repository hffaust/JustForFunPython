import sys
import click
from pytube import YouTube

def read_video_list(filename, delimiter):
    f = open(filename,'r')
    content = f.read()
    print(content)
    if(delimiter != None):
        content = content.split(delimiter)
    print(content)
    f.close()
    return content

def download_from_youtube(urls, audio_only=False, save_captions=False, interactive_mode=False):
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
                stream.download()
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
def main(video_list_filename,list_delimiter,url,audio_only,save_captions,interactive_mode):
    urls = []
    if(video_list_filename != None):
        urls.extend( read_video_list(video_list_filename, list_delimiter) )
    if(url != None):
        print(url)
        urls.append(url)
    print(urls)
    download_from_youtube(urls, audio_only=audio_only, save_captions=save_captions, interactive_mode=interactive_mode)
    print("ALL DONE")
    return 0


if __name__ == "__main__":
    main()
