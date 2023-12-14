import os
import subprocess

input_dir = cwd = os.getcwd()
current_dir = os.getcwd()
parent_dir_name = os.path.basename(os.path.dirname(current_dir))  

output_dir = f'C:\\Users\\Vejituh\\Videos\\{parent_dir_name}-final'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for filename in os.listdir(input_dir):
    if filename.lower().endswith(('.py', '.bat')):
        print('ignore')
    else:
        input_path = os.path.join(input_dir, filename)
        base_name = os.path.splitext(filename)[0] 
        output_path = os.path.join(output_dir, base_name + ".mkv")

        # Get video codec 
        result = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                                '-show_entries', 'stream=codec_name', '-of', 
                                'default=nokey=1:noprint_wrappers=1', input_path],
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        # Get audio codec 
        result_audio = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a:0',
                                '-show_entries', 'stream=codec_name', '-of', 
                                'default=nokey=1:noprint_wrappers=1', input_path],
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        # Get audio channel 
        result_audio_channels = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a:0',
                                '-show_entries', 'stream=channels', '-of', 
                                'default=nokey=1:noprint_wrappers=1', input_path],
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        video_codec = result.stdout.decode('utf-8').strip()
        audio_codec = [result_audio.stdout.decode('utf-8').strip(), result_audio_channels.stdout.decode('utf-8').strip()]


        if video_codec not in ["h264", "hevc"]:
            video_args = ['-c:V', 'libx264', '-crf', '25'] 
        else:
            video_args = ['-c:V', 'copy']
        
        if audio_codec not in [["aac", "2"]]:
            audio_args = ['-map', '0:a', '-c:a', 'aac', '-b:a', '128k','-ac', '2'] 
        else:
            audio_args = ['-map', '0:a', '-c:a', 'copy']
        subtitle_args = ['-map', '0:s?', '-c:s', 'copy']
        
        encode_command = ['ffmpeg',
                        '-i', input_path,
                        '-map', '0:V:0', 
                        *video_args,
                        *audio_args,
                        *subtitle_args,
                        output_path]

        subprocess.run(encode_command)
        os.remove(filename)

    print('Complete!')
