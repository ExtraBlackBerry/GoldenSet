import re

def to_json(script, objects, sentiment, qa_pairs):
    qa_pairs_json = [
        {"question": q.strip(), "answer": a.strip()}
        for q, a in re.findall(r"Question:(.*?)Answer:(.*?)(?=\d+\.|$)", qa_pairs, re.S)
    ]

    return {
        "transcript": script,
        "objects": objects,
        "sentiment": sentiment,
        "qa_pairs": qa_pairs_json
    }

#unit test
if __name__ == "__main__":
    sample_script = "This is a sample transcript."
    sample_objects = ["cat", "dog", "car"]
    sample_sentiment = "Positive"
    sample_qa_pairs = "1. Question: What is this? Answer: This is a test. 2. Question: How are you? Answer: I am fine."

    result = to_json(sample_script, sample_objects, sample_sentiment, sample_qa_pairs)
    print(result)