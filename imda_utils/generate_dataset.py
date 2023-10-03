from zipfile import ZipFile
import glob
import os, shutil
import librosa
import soundfile as sf

## Generate wav files and filelists from the IMDA dataset.
def process_wavs():
    # remove all files if we are regenrating the folder.
    empty_folder(OUT_PATH)

    wav_contents = glob.glob(FULL_WAV_PATH)
    for speaker in wav_contents:
        with ZipFile(speaker, 'r') as zObject:
            for item in zObject.filelist:
                if '.WAV' in item.filename:
                    zObject.extract(item.filename, path = OUT_PATH)
            ## Move all the files.
            wavs_in_subfolders = glob.glob(f"{OUT_PATH}/**", recursive=True)
            for wav_file in wavs_in_subfolders:
                if '.WAV' in wav_file:
                    new_name = OUT_PATH + "\\"  + wav_file.split('\\')[-1]
                    os.rename(wav_file, new_name) ## move file
                # Remove all subfolders
            try:
                shutil.rmtree(f"{OUT_PATH}/{SPEAKER_PATH}{SPEAKER_NUM}")
            except FileNotFoundError:
                print(f"FileNotFoundError when trying to remove {OUT_PATH}/{SPEAKER_PATH}{SPEAKER_NUM}")

            zObject.close()

    for root, _, files in os.walk(OUT_PATH):
        for f in files:
            resampled_audio , sr = librosa.load(os.path.join(root, f), sr = 22050)
            sf.write(f"{OUT_PATH}/{f}", resampled_audio, samplerate=22050)
    
    # print(wavs_list)
    print("wavs for speaker generated!")


def create_transcript():
    OUT_WAV_PATH_CONTENTS = glob.glob(f"{OUT_PATH}/**")
    script_counter = 0
    # print("OUT_WAV_PATH_CONTENTS = ", OUT_WAV_PATH_CONTENTS[:10])
    with open(f"{OUT_SCRIPT_PATH}/{SPEAKER_PATH}{SPEAKER_NUM}.txt", "w") as outFile:
        for script in SCRIPTS:
            full_scripts_path = f"{DATASET_PATH}/{AUDIO_PATH}/{CHANNEL_NUM}/{SCRIPT_DIR_PATH}/{script}"
            print("full_script_path = "+ full_scripts_path)
            with open(full_scripts_path, 'r') as srcFile:
                lines = srcFile.readlines()
                for line in lines:
                    if (script_counter >= len(OUT_WAV_PATH_CONTENTS)):
                        break
                    
                    fragments = line.split('\t')
                    audio_file_path = OUT_WAV_PATH_CONTENTS[script_counter].split('\\')[-1]
                    print("audio_file_path = ", audio_file_path)
                    print("fragments[0].wav=", f"{fragments[0]}.WAV")
                    if (audio_file_path in f"{fragments[0]}.WAV"):
                        script_counter += 1
                        # Write to out file
                        outFile.write(f"{audio_file_path}|{fragments[1]}")

    print("Total matches = ", script_counter)

def empty_folder(path: str):
    for root, dir, files in os.walk(path):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dir:
            shutil.rmtree(os.path.join(root, d))
    print(f"{path} folder emptied!") 

if __name__ == "__main__":

    DATASET_PATH = r"C:\Users\teoju\Dropbox\IMDA - National Speech Corpus"
    OUT_PATH = r"C:\Users\teoju\OneDrive\Desktop\SMU_Code\SMU_Research\Text-to-Speech\tacotron2-nvidia\wavs"
    OUT_SCRIPT_PATH = r"C:\Users\teoju\OneDrive\Desktop\SMU_Code\SMU_Research\Text-to-Speech\tacotron2-nvidia\filelists"

    AUDIO_PATH = r"PART1/DATA"
    CHANNEL_NUM = r"CHANNEL0"
    WAV_PATH = "WAVE"

    SPEAKER_PATH = r"SPEAKER"
    SPEAKER_NUM = r"0002"

    SCRIPT_DIR_PATH = "SCRIPT"
    SCRIPTS = ["000020.TXT", "000021.TXT"]

    FULL_WAV_PATH = f"{DATASET_PATH}/{AUDIO_PATH}/{CHANNEL_NUM}/{WAV_PATH}/{SPEAKER_PATH}{SPEAKER_NUM}*"

    wav_contents = glob.glob(FULL_WAV_PATH)
    process_wavs()

    create_transcript()
    
    # print("OUT_WAV_PATH_CONTENTS = ", OUT_WAV_PATH_CONTENTS[:10])

                    # print("fragments = ", fragments)
    