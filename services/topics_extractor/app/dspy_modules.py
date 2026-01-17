import dspy
from typing import List, Dict
from app.models import Topic, TopicTree, TopicMetadata


class TopicExtractor(dspy.Signature):
    """Extract the topics from the given text make sure to take only topics and not just headers. 
    return a list of the topics according to the Topic model with the topic input.
      make sure to avoid duplicates and keep the most relevant ones.
      meaning, if a topic or a similar one already exists in the topics_input, don't add it again.
      return only new topics(the delta) that are not in the topics_input.
      """

    topics_input: List[Topic] | None = dspy.InputField(desc="A list of topics that we've extracted so far.")
    source_file: str | None = dspy.InputField(desc="The name of the file the text was extracted from. use for metadata")
    text: str = dspy.InputField()
    topics_output: List[Topic] = dspy.OutputField(desc="A list of the most relevant topics extracted from the given text in the given structure including the metadata, confidence_score should be from 0 to 1, .")


class TopicTreeGenerator(dspy.Signature):
    """Generate a hierarchical topic tree from the given flat list of topics. Make sure to group similar topics under broader ones."""

    topics: List[Topic] = dspy.InputField()
    topic_tree: TopicTree = dspy.OutputField(desc="A hierarchical tree structure of topics generated from the flat list of topics.")


class UpdateTopicTree(dspy.Signature):
    """Update the given topic tree with new topics, integrating them appropriately into the existing hierarchy."""

    existing_topic_tree: TopicTree = dspy.InputField()
    new_topics: List[Topic] = dspy.InputField()
    updated_topic_tree: TopicTree = dspy.OutputField(desc="The updated topic tree with the new topics integrated, don't remove existing topics and don't add duplicates.")

class MaterialToTopicMatcher(dspy.Signature):
    """Match the given material to its most relevant topics, try to be as specific as possible and merge similar topics."""

    material: str = dspy.InputField()
    topics: List[Topic] = dspy.InputField()
    matched_topics: List[Topic] = dspy.OutputField(desc="The most relevant topics to the given material from the given list of topics.")