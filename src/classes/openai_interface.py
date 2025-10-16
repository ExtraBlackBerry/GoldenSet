import base64
from pyexpat import model
from xmlrpc import client
from dotenv import load_dotenv
import os
from openai import OpenAI
import cv2
from scenedetect import open_video, SceneManager
from scenedetect.detectors import ContentDetector

#Make sure to create a .env file with your OPENAI_API_KEY
class OpenAIInterface:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def frame_to_base64(self, frame):
         _, buffer = cv2.imencode(".jpg", frame)
         return base64.b64encode(buffer).decode("utf-8")

    def image_analysis(self, frame, context):
        if context == "":
            return "No context provided"
        image_base64 = self.frame_to_base64(frame)
        response = self.client.chat.completions.create(
            model = "gpt-4o",
            messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""You are analyzing frames from a video.

                                    Video Script Context:
                                    {context}

                                    Your task:
                                    - Identify and list all visible objects in the image(s).
                                    - Use simple object names (e.g., "knife", "steak", "pan", "person", "table").
                                    - List all objects that are visible.
                                    - Do NOT describe the scene or actions.
                                    - Do NOT include any text or reasoning, only the list.

                                    Output format:
                                    object1, object2, object3
                                    """
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    },
                ],
            }
        ],
    )
        return response.choices[0].message.content

    def is_scene_change(frame1, frame2, threshold=0.7):
        hist1 = cv2.calcHist([frame1], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        hist2 = cv2.calcHist([frame2], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])

        cv2.normalize(hist1, hist1)
        cv2.normalize(hist2, hist2)
        
        similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
        return similarity < threshold
    
    def detect_scenes(self,video_path ,script, threshold=40.0):
        if script == "":
            return "No context provided"
        video = open_video(video_path)
        manager = SceneManager()
        manager.add_detector(ContentDetector(threshold=threshold))
        manager.detect_scenes(video)
        scenes = manager.get_scene_list()
        cap = cv2.VideoCapture(video_path)
        object_list = []
        for i, scene in enumerate(scenes):
            start_frame = int(scene[0].get_frames())
            start_time = scene[0].get_timecode()

            cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
            ret, frame = cap.read()

            description = self.image_analysis(frame, script)
            items = [item.strip() for item in description.split(", ")]
            for item in items:
                if item not in object_list:
                    object_list.append(item)
 

        cap.release()
        return object_list
    
    def analyze_sentiment(self, transcript):
        if transcript == "":
            return "No context provided"
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": f"""Analyze the sentiment of the following text and classify it as Positive, Negative, or Neutral. Provide a brief explanation for your classification.

                    Text: {transcript}
                    """
                }
            ]
        )
        return (response.choices[0].message.content)

    def generate_qa_pairs(self, transcript, object):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": f"""
                        You are an AI assistant. Generate what you believe would be most commonly asked Question-Answer pairs based on this transcript of a video and object list.
                        Each pair should reflect information that someone could learn by watching the video. Make sure you only use the given information.

                        Transcript:
                        {transcript}
                        objects:
                        {object}

                        Return the output as comma separated array like:
                        1. Question: Answer,
                        2. Question: Answer...
                        """
                }
            ]
        )

        return response.choices[0].message.content


#unit test
if __name__ == "__main__":
    openai_interface = OpenAIInterface()
    sentiment = openai_interface.analyze_sentiment("I love programming!")
    print("Sentiment Analysis:", sentiment)

    qa = openai_interface.generate_qa_pairs("This is a sample transcript about cooking pasta.", ["pasta", "pot", "water"])
    print("Generated Q&A Pairs:", qa)

    video_path = r"video\AI_Intern_Project.mp4"
    script = "This is a sample transcript about cooking pasta."
    objects = openai_interface.detect_scenes(video_path, script)
    print("Detected Objects:", objects)