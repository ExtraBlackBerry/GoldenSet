from classes.openai_interface import OpenAIInterface
from classes.transcribe import Transcriber
from classes.to_json import to_json
import json

if __name__ == "__main__":
    video_path = r"video\AI_Intern_Project.mp4"

    openai_interface = OpenAIInterface()
    transcriber = Transcriber(video_path)
    
    script = transcriber._transcribe_audio()
    object_list = openai_interface.detect_scenes(video_path, script)
    sentiment = openai_interface.analyze_sentiment(script)
    qa = openai_interface.generate_qa_pairs(script, object_list)

    json_data = to_json(script, object_list, sentiment, qa)

    with open("final_output.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)