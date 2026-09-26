"""
Service Vocal (Azure Speech) d'EPFind.

Deux fonctions :
- transcribe_audio()  : voix -> texte
- synthesize_speech() : texte -> voix

Le navigateur envoie du WebM/Opus.
On le convertit en WAV PCM 16 kHz mono avant de l'envoyer à Azure.
"""

import io
import os
import wave

import av
import requests
from dotenv import load_dotenv

load_dotenv()

AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")


def _check_config():
    if not AZURE_SPEECH_KEY:
        raise ValueError("AZURE_SPEECH_KEY est manquant dans .env")
    if not AZURE_SPEECH_REGION:
        raise ValueError("AZURE_SPEECH_REGION est manquant dans .env")


def transcribe_audio(audio_bytes: bytes, language: str = "fr-FR") -> str:
    """
    Convertit le WebM/Opus du navigateur en WAV PCM 16 kHz mono,
    puis envoie l'audio à Azure Speech-to-Text.
    """
    _check_config()

    # WebM/Opus -> PCM 16 kHz mono
    container = av.open(io.BytesIO(audio_bytes))
    stream = container.streams.audio[0]

    resampler = av.audio.resampler.AudioResampler(
        format="s16",
        layout="mono",
        rate=16000,
    )

    frames = []

    for packet in container.demux(stream):
        for frame in packet.decode():
            frames.extend(resampler.resample(frame))

    wav_buffer = io.BytesIO()

    with wave.open(wav_buffer, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(16000)

        for frame in frames:
            wav.writeframes(frame.to_ndarray().tobytes())

    wav_buffer.seek(0)

    # Envoi du WAV à Azure
    url = (
        f"https://{AZURE_SPEECH_REGION}.stt.speech.microsoft.com"
        f"/speech/recognition/conversation/cognitiveservices/v1"
        f"?language={language}"
    )

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_SPEECH_KEY,
        "Content-Type": "audio/wav; codecs=audio/pcm; samplerate=16000",
        "Accept": "application/json",
    }

    response = requests.post(
        url,
        headers=headers,
        data=wav_buffer.read(),
        timeout=30,
    )

    if response.status_code != 200:
        raise ValueError(
            f"Erreur Azure Speech-to-Text ({response.status_code}) : {response.text}"
        )

    result = response.json()

    if result.get("RecognitionStatus") != "Success":
        raise ValueError(
            "La voix n'a pas été reconnue, réessaie plus près du micro."
        )

    return result.get("DisplayText", "")


def synthesize_speech(text: str, language: str = "fr-FR") -> bytes:
    """
    Envoie du texte à Azure Text-to-Speech et retourne un audio MP3.
    """
    _check_config()

    url = (
        f"https://{AZURE_SPEECH_REGION}.tts.speech.microsoft.com"
        f"/cognitiveservices/v1"
    )

    voice_name = (
        "fr-FR-DeniseNeural"
        if language.startswith("fr")
        else "en-US-JennyNeural"
    )

    ssml = f"""<speak version='1.0' xml:lang='{language}'>
<voice xml:lang='{language}' name='{voice_name}'>{text}</voice>
</speak>"""

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_SPEECH_KEY,
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "audio-16khz-32kbitrate-mono-mp3",
    }

    response = requests.post(
        url,
        headers=headers,
        data=ssml.encode("utf-8"),
        timeout=30,
    )

    if response.status_code != 200:
        raise ValueError(
            f"Erreur Azure Text-to-Speech ({response.status_code}) : {response.text}"
        )

    return response.content
