GoldenSet Technical Assessment Project

Goal
Process the video attached to this email, the output should be in JSON format and include these information
Video's complete Transcription
As many Objects detected in video
The over all mode and sentiment of the video
Convert video's transcript to list of QA pairs about the video

Approach

I divided the problem to each sections

    Video Transcription.

    Object Identification.

    Identifying Mode and Sentiment.

    Match Transcript to answer Questions about the video.

1. Video Transcription

   When I watched the video there are many background noises (eg. cooking noise, music).
   I went to look at methods on how I could isolate voice from the video.(ChatGPT, Google)

   Spleeter, Demucs,Audio Seperator seems to be the most commonly utilised.
   For our usecase we will use Audio Seperator as it is light weight (Would use Demucs or other higher performing methods in production envrionment)

   Now that we have isolated the voice we will be using whisper by openAI to extract the text.
   Whisper (OPEN AI) is a easy to use free model that is also small and very fast.

2. Object Identification

   This is when I started looking into OpenAI's available APIs
   They have a image and vision section where it utilizes OpenAI's model to describe or analyze a specific scene/image.
   One problem I wanted to try and tackle is the token usage. Because if we analyze the image every frame that would be requesting minimum 30 times a second. This is where I thought why not try and identify the object when the current frame is different from previous frame by comparing them using computer vision. Reducing the token usage

   I also wanted to give the AI more context by sending the transcribed text for more accurate object detection.

   I decided to go with lightweight option comparing the histograms of current and previous frame.

3. Identifying Mood and Sentiment. Match Transcript to answer Questions about the video.

   I simply used prompt engineering and for question answer pairs I made sure the AI only uses given context without using external information.

How much AI did you use?
I used copilot and used ChatGPT to do research related to each section and to generate early prompt designs before I edited them.

In your opinion, where are the places you could do better?
I could improve on more cleaner code and better documentation.
Along side I could also improve the speed of the application by optimizing the code.
