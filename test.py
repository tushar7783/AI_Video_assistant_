# from utils.audio_processor import download_youtube_audio ,convert_to_wav,chunk_audio
import traceback
from utils.audio_processor import process_input
from core.transcriber import transcribe_all

if __name__=='__main__':
    try:
        url="https://www.youtube.com/shorts/qGL05qUFQTM"
        # # download_youtube_audio(url)
        # data =download_youtube_audio(url)
        # # print(convert_to_wav(data))
        # converted_wax=convert_to_wav(data)
        # print(chunk_audio(converted_wax,3))
        # print(process_input(url))
        chunks_list=process_input(url)
        language="hinglish"
        print(transcribe_all(chunks_list,language=language))
          
        
    except Exception:
        traceback.print_exc()


