import importlib
import sys
import types
import tempfile
import os
import pytest

print(os.getcwd())
from app.md_loader import load_markdown_file
from app.render_topic_tree import build_html


def test_load_markdown_file_reads(tmp_path):
    p = tmp_path / "sample.md"
    content = "# Hello\nThis is a test"
    p.write_text(content, encoding='utf-8')
    assert load_markdown_file(str(p)) == content


def test_load_markdown_file_missing(tmp_path):
    missing = tmp_path / "nope.md"
    with pytest.raises(RuntimeError):
        load_markdown_file(str(missing))


def test_render_topic_tree_build_html():
    tree = {"topic": {"name": "root", "description": "desc"}}
    html = build_html(tree)
    assert "<!doctype html>" in html
    assert 'root' in html


def test_dspy_adapter_functions_with_fake_dspy(monkeypatch):
    # Create a fake dspy module to avoid external dependency at import time
    fake = types.ModuleType("dspy")

    setattr(fake, "LM", lambda model, api_key=None: None)
    setattr(fake, "configure", lambda lm=None: None)
    setattr(fake, "Signature", type("Signature", (object,), {}))
    setattr(fake, "InputField", lambda *a, **k: None)
    setattr(fake, "OutputField", lambda *a, **k: None)

    def Predict(sig):
        class Predictor:
            def __call__(self, **kwargs):
                name = getattr(sig, "__name__", "")
                if name == "TopicExtractor":
                    return {"topics_output": [{"name": "T1"}]}
                if name == "TopicTreeGenerator":
                    return {"topic_tree": {"topic": {"name": "root"}}}
                if name == "UpdateTopicTree":
                    return {"updated_topic_tree": {"topic": {"name": "root"}}}
                if name == "MaterialToTopicMatcher":
                    return {"matched_topics": [{"name": "T1"}]}
                return {}
        return Predictor()

    setattr(fake, "Predict", Predict)

    # Insert into sys.modules so importing app.dspy_adapter uses the fake module
    sys.modules["dspy"] = fake

    # Ensure local modules are importable under their plain names so
    # top-level imports inside package modules resolve correctly.
    sys.modules["models"] = importlib.import_module("app.models")
    sys.modules["dspy_modules"] = importlib.import_module("app.dspy_modules")
    sys.modules["settings"] = importlib.import_module("app.settings")

    # Reload the adapter module to pick up the fake dspy
    da = importlib.reload(importlib.import_module("app.dspy_adapter"))

    assert da.extract_topics_from_texts("some text") == [{"name": "T1"}]
    assert da.generate_topic_tree([]) == {"topic": {"name": "root"}}
    assert da.update_topic_tree({"topic": {"name": "root"}}, []) == {"topic": {"name": "root"}}
    assert da.match_topics_to_material("text", []) == [{"name": "T1"}]
