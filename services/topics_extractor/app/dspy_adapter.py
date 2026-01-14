import re
from typing import Optional
from dspy_modules import (TopicExtractor, MaterialToTopicMatcher, List, Dict, dspy, Topic, TopicTreeGenerator, TopicTree, UpdateTopicTree, TopicMetadata)
import os
from settings import Settings

settings = Settings()

lm = dspy.LM(settings.lm_model, api_key=settings.lm_api_key)
dspy.configure(lm=lm)


def extract_topics_from_texts(text: str, file_name: Optional[str] = None):
    topic_extractor = dspy.Predict(TopicExtractor)
    return topic_extractor(text=text, source_file=file_name, topics_input=[]).get("topics_output")


def generate_topic_tree(topics: Optional[List[Topic]]):
    topic_tree_generator = dspy.Predict(TopicTreeGenerator)
    return topic_tree_generator(topics=topics).get("topic_tree")


def update_topic_tree(existing_tree: TopicTree, new_topics: List[Topic]) -> TopicTree | None:
    topic_updater = dspy.Predict(UpdateTopicTree)
    return topic_updater(existing_topic_tree=existing_tree, new_topics=new_topics).get("updated_topic_tree")


def match_topics_to_material(text: str, topics: List[Topic]) -> List[Topic] | None:
    topic_matcher = dspy.Predict(MaterialToTopicMatcher)
    return topic_matcher(material=text, topics=topics).get("matched_topics")