
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

def denoise(audio_path: str) -> str:
    """Dénoise un fichier audio en utilisant le CPU ou le GPU selon la disponibilité."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = pretrained.dns64().to(device)

    # Charger et convertir l'audio
    wav, sr = torchaudio.load(audio_path)
    wav = convert_audio(wav, sr, model.sample_rate, model.chin).to(device)

    # Dénoiser
    with torch.no_grad():
        denoised = model(wav[None])[0].cpu()  # Assurez-vous de ramener en CPU pour torchaudio.save

    # Sauvegarde du fichier
    denoised_path = audio_path.replace('.wav', '_denoised.wav')
    torchaudio.save(denoised_path, denoised, model.sample_rate)
    return denoised_path
