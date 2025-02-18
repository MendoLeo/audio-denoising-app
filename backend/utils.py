
import os
import subprocess
import torchaudio
import torch
from denoiser import pretrained
from denoiser.dsp import convert_audio

#Utility functions
def convert_to_wav(pcm_file: str, output_dir: str)-> str:
    """
    convert_to_wav _summary_

    Args:
        pcm_file (str): pcm audio_dir
        output_dir (str): wav audio_dir

    Returns:
        str: wav output_dir
    """
    
    wav_file = os.path.join(output_dir, os.path.basename(pcm_file).replace('.pcm', '.wav'))
    command = ["ffmpeg", "-f", "s16le", "-ar", "44100", "-ac", "1", "-i", pcm_file, wav_file, "-y"]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return wav_file


def convert_to_opus(wav_file, output_dir):
    """
    convert_to_opus _summary_

    Args:
        wav_file (str): audio path
        output_dir (str): convert opus audio path

    Returns:
        str: opus output_dir
    """

    opus_file = os.path.join(output_dir, os.path.basename(wav_file).replace('.wav', '.opus'))
    command = ["ffmpeg", "-i", wav_file, "-c:a", "libopus", opus_file, "-y"]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return opus_file

def denoise(audio_path: str)-> str:
    """
    denoiser : this function remove background noise on input audio and produce donoising audio

    Args:
        audio_path (str): _description_

    Returns:
        str: _description_
    """
    model = pretrained.dns64()
    wav, sr = torchaudio.load(audio_path)
    wav = convert_audio(wav, sr, model.sample_rate, model.chin)

    with torch.no_grad():
        denoised = model(wav[None])[0]

    denoised_path = audio_path.replace('.wav', '_denoised.wav')
    torchaudio.save(denoised_path, denoised.cpu(), model.sample_rate)

    return denoised_path

#################### CAS D'USAGE D'UN ACCELERATEUR #################################

"""model = pretrained.dns64().cuda()
wav, sr = torchaudio.load(audio_path)
wav = convert_audio(wav.cuda(), sr, model.sample_rate, model.chin)
"""