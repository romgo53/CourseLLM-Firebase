import dspy
from typing import List, Dict
from models import Topic, TopicTree


class TopicExtractor(dspy.Signature):
    """Extract the topics from the given text make sure to take only topics and not just headers. return a list of the topics with combined with the input topics. make sure to avoid duplicates and keep the most relevant ones."""

    topics_input: List[str] | None = dspy.InputField(desc="A list of topics that we've extracted so far.")
    text: str = dspy.InputField()
    topics_output: List[Topic] = dspy.OutputField(desc="A list of the most relevant topics extracted from the given text in the given structure, combined with the input topics.")


class TopicTreeGenerator(dspy.Signature):
    """Generate a hierarchical topic tree from the given flat list of topics. Make sure to group similar topics under broader ones."""

    topics: List[Topic] = dspy.InputField()
    topic_tree: TopicTree = dspy.OutputField(desc="A hierarchical tree structure of topics generated from the flat list of topics.")

class MaterialToTopicMatcher(dspy.Signature):
    """Match the given material to its most relevant topics, try to be as specific as possible and merge similar topics."""

    material: str = dspy.InputField()
    topics: List[Topic] = dspy.InputField()
    matched_topics: List[Topic] = dspy.OutputField(desc="The most relevant topics to the given material from the given list of topics.")