from project import parse_flashcards
from project import get_ai_response
from project import save_to_pdf
from unittest.mock import patch
import requests
import json


def test_parse_flashcards():

    text = json.dumps([
        {
            "question": "What is AI?",
            "answer": "Artificial Intelligence"
        },
        {
            "question": "What is Machine Learning?",
            "answer": "A subset of AI"
        },
        {
            "question": "What is Deep Learning?",
            "answer": "A neural-network-based approach"
        }
    ])

    expected = [
        ("What is AI?", "Artificial Intelligence"),
        ("What is Machine Learning?", "A subset of AI"),
        ("What is Deep Learning?", "A neural-network-based approach")
    ]

    assert parse_flashcards(text) == expected



def test_parse_flashcards_empty():
    assert parse_flashcards(None) == []



def test_parse_flashcards_invalid():
    assert parse_flashcards("not json") == []


@patch("project.requests.post")
def test_get_ai_response_success(mock_post):

    fake_json = {
        "choices": [
            {
                "message": {
                    "content": "Fake flashcard response"
                }
            }
        ]
    }

    mock_post.return_value.json.return_value = fake_json
    mock_post.return_value.raise_for_status.return_value = None

    result = get_ai_response("Python")

    assert result == "Fake flashcard response"


@patch("project.requests.post")
def test_get_ai_response_failure(mock_post):

    mock_post.side_effect = requests.exceptions.RequestException

    result = get_ai_response("Python")

    assert result is None


def test_save_to_pdf(tmp_path):

    cards = [
        ("What is AI?", "Artificial Intelligence"),
        ("What is Python?", "A programming language")
    ]

    filename = tmp_path / "flashcards.pdf"

    result = save_to_pdf(cards, str(filename))

    assert result is True
    assert filename.exists()