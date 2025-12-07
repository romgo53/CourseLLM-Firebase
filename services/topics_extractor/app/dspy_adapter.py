import re
from dspy_modules import (TopicExtractor, MaterialToTopicMatcher, List, Dict, dspy)
import os

lm = dspy.LM(os.environ.get("LM_MODEL", "gemini/gemini-2.5-flash"), api_key=os.environ.get("LM_API_KEY", ""))

async def extract_topics_from_texts(text: str) -> List[str]:
    topic_extractor = dspy.Predict(TopicExtractor)
    return topic_extractor(text=text).get("topics")


async def match_topics_from_to_material(text: str, topics: List[str]) -> List[str]:
    topic_matcher = dspy.Predict(MaterialToTopicMatcher)
    return topic_matcher(material=text, topics=topics).get("matched_topics")