# from utils.audio_processor import download_youtube_audio ,convert_to_wav,chunk_audio
from utils.audio_processor import process_input


if __name__=='__main__':
    try:
        url="https://www.youtube.com/watch?v=VSFuqMh4hus"
        # # download_youtube_audio(url)
        # data =download_youtube_audio(url)
        # # print(convert_to_wav(data))
        # converted_wax=convert_to_wav(data)
        # print(chunk_audio(converted_wax,3))
        print(process_input(url))
        
    except Exception as e:
        print(e)


