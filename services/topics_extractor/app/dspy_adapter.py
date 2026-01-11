import re
from typing import Optional
from dspy_modules import (TopicExtractor, MaterialToTopicMatcher, List, Dict, dspy, Topic, TopicTreeGenerator, TopicTree)
import os


lm = dspy.LM(os.environ.get("LM_MODEL", "gemini/gemini-2.5-flash"), api_key=os.environ.get("LM_API_KEY", ""))
dspy.configure(lm=lm)


def extract_topics_from_texts(text: str):
    topic_extractor = dspy.Predict(TopicExtractor)
    return topic_extractor(text=text, topics_input=[]).get("topics_output")


def generate_topic_tree(topics: Optional[List[Topic]]):
    topic_tree_generator = dspy.Predict(TopicTreeGenerator)
    return topic_tree_generator(topics=topics).get("topic_tree")


def match_topics_to_material(text: str, topics: List[Topic]) -> List[Topic] | None:
    topic_matcher = dspy.Predict(MaterialToTopicMatcher)
    return topic_matcher(material=text, topics=topics).get("matched_topics")