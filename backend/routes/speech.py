"""
Routes vocales : POST /speech/transcribe et POST /speech/synthesize
Responsable : Personne 3.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

from backend.services.speech_service import transcribe_audio, synthesize_speech

router = APIRouter()


@router.post("/speech/transcribe")
async def transcribe(file: UploadFile = File(...)):
    """Reçoit l'enregistrement du micro et retourne le texte reconnu."""
    try:
        audio_bytes = await file.read()

        text = transcribe_audio(audio_bytes)
        return {"text": text}
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except Exception as error:
        raise HTTPException(
            status_code=500, detail=f"Erreur pendant la reconnaissance vocale : {str(error)}"
        )


class SynthesizeRequest(BaseModel):
    text: str
    language: str = "fr-FR"


@router.post("/speech/synthesize")
def synthesize(request: SynthesizeRequest):
    """Reçoit un texte et retourne un fichier audio MP3 à jouer."""
    try:
        audio_bytes = synthesize_speech(request.text, request.language)
        return Response(content=audio_bytes, media_type="audio/mpeg")
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except Exception as error:
        raise HTTPException(
            status_code=500, detail=f"Erreur pendant la synthèse vocale : {str(error)}"
        )
