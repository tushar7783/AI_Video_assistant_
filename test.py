# from utils.audio_processor import download_youtube_audio ,convert_to_wav,chunk_audio
import traceback
from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarizer import split_transcript ,generate_title,summarize
from core.extractor import extract_action_items,extract_key_decisions,extract_questions
if __name__=='__main__':
    try:
        url="https://www.youtube.com/watch?v=pN-LfxNFiTc"
        # # download_youtube_audio(url)
        # data =download_youtube_audio(url)
        # # print(convert_to_wav(data))
        # converted_wax=convert_to_wav(data)
        # print(chunk_audio(converted_wax,3))
        # print(process_input(url))
        # chunks_list=process_input(url)
        # language="hinglish"
        # print(transcribe_all(chunks_list,language=language))
        # text='''
        # Lorem ipsum dolor sit amet consectetur adipisicing elit. Odio 
        # magnam dignissimos reprehenderit. Sint dignissimos harum assumenda, at
        #  repellat eum temporibus molestias aspernatur amet veritatis.
        #   Reprehenderit dicta delectus similique tenetur repellendus?

        # '''
        # print(split_transcript(text))
        # transcribe=
        '''
The Clockmaker of Oakhaven

The brass gears of the Great Pendulum did not merely tick; they breathed.
In the high, vaulted attic of the Oakhaven clock tower, Julian spent his nineteenth winter greasing pinions and balancing escapement wheels. Outside, the slate-grey roofs of the village were buried under three feet of January snow. Inside, the air smelled of machine oil, dried lavender, and centuries of accumulated dust.
Julian’s grandfather had left him the tower with a single instruction: “Never let the central weight touch the floor, Julian. If the town clock stops, the pulse stops.”
As a child, Julian had taken it as an old man’s poetic nonsense—a metaphor for civic punctuality. The bakers needed to know when to pull the sourdough; the blacksmith needed to gauge the morning hearth. Yet, as Julian grew older, he noticed strange things. When the pendulum slowed during a severe frost three winters ago, the villagers moved sluggishly, their speech dragging like a groaning spring. When Julian cleaned the main gear and restored the rhythmic tick-tock, a sudden, bright energy seemed to ripple back into the cobblestone streets below.
The clock did not just tell time in Oakhaven. It governed it.
That evening, the wind howled down the stairwell, carrying a sharp, metallic tang that did not belong to the gears. Julian paused, a brass oiler poised over the pallet fork.
The pendulum gave a sickening, heavy thud—not a tick, nor a tock, but a wet, leaden hitch.
Upstairs, in the glass-domed observatory above the gearroom, the secondary dials began to spin backward. Julian dropped the oiler, his boots clattering against the spiral iron staircase as he sprinted to the summit.
The dome was frosted over from the outside, moonlight cutting through the rime to cast jagged, pale geometry across the floor. Standing beside the Master Dial was a stranger.
She wore a heavy travel cloak the color of wet slate, its hem caked in frozen mud. Her fingers—long, ink-stained, and bare of gloves—were pressed directly against the glass of the frozen dial, tracing a small, glowing rune that Julian had never carved into the brass.
"Step away from the regulator," Julian said, his voice cracking slightly in the thin air. He gripped a heavy iron winding crank like a mace.
The stranger did not startle. She turned slowly, her face illuminated by the amber glow of the internal counterweights. Her eyes were not brown or blue, but the pale, translucent amber of old clock crystals.
        # '''
        chunks_list=process_input(url)

        language="english"
        transcribe=transcribe_all(chunks_list,language=language)
        print("\n"+"="*60)
        print("transcribe")
        print("\n"+"="*60)
        tittle=generate_title(transcribe)
        summary=summarize(transcribe)
        action_items=extract_action_items(transcribe)
        decision=extract_key_decisions(transcribe)
        questions=extract_questions(transcribe)


        print("\n"+"="*60)
        print (summary)
        print("\n"+"="*60)

        print("ACTION ITEMS")
        print("="*60)
        print(action_items)
        print("\n"+"="*60)
        
        print("key decision")
        print("="*60)
        print(decision)
        print("\n"+"="*60)
        
        print("open question")
        print("="*60)
        print(questions)
        
        





        # print(summarize(transcribe))
        # print(generate_title())
        # chunks_list=process_input(url)
        # transcribe_text=transcribe_all(chunks_list,language=language)






          
        
    except Exception:
        traceback.print_exc()


