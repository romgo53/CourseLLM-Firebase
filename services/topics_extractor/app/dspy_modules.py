import dspy
from typing import List, Dict
from md_loader import load_markdown_file



class TopicExtractor(dspy.Signature):
    """Extract the topics from the given text make sure to take only topics and not just headers. return a list of the topics with combined with the input topics. make sure to avoid duplicates and keep the most relevant ones."""

    topics_input: List[str] = dspy.InputField(desc="A list of topics that we've extracted so far.")
    text: str = dspy.InputField()
    topics_output: List[str] = dspy.OutputField(desc="A list of the most relevant topics extracted from the given text, combined with the input topics.")


class MaterialToTopicMatcher(dspy.Signature):
    """Match the given material to its most relevant topics, try to be as specific as possible and merge similar topics."""

    material: str = dspy.InputField()
    topics: List[str] = dspy.InputField()
    matched_topics: List[str] = dspy.OutputField(desc="The most relevant topics to the given material from the given list of topics.")
