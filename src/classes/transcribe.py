from audio_separator.separator import Separator
import whisper

class Transcriber:
    def __init__(self, video_path=None):
        self._separator = Separator()
        self._video_path = video_path
        self._audio_path = None
        self._whisper_model = whisper.load_model("small")

    def _separate_audio(self):
        if not self._video_path:
            raise ValueError("Video path is not set.")
        self._separator.load_model(
            model_filename="mel_band_roformer_karaoke_aufr33_viperx_sdr_10.1956.ckpt"
        )  
        _result = self._separator.separate(self._video_path)
        self._audio_path = _result[1]
        return _result[1]

    def _transcribe_audio(self):
        self._separate_audio()
        if not self._audio_path:
            raise ValueError("Audio path is not set.")
        result = self._whisper_model.transcribe(self._audio_path)
        return result["text"]
       

#unit test
if __name__ == "__main__":
    #seperate audio
    transcriber = Transcriber(r"video\AI_Intern_Project.mp4")
    transcriber._separate_audio()

    transcriber = Transcriber(r"video\AI_Intern_Project.mp4")
    transcriber._transcribe_audio()