# tests/test.py
import pytest
from unittest.mock import patch, MagicMock
from model import Model
from metrics import Metrics

# Model.get_name tests
def test_get_name_code_basic():
    m = Model("", "", "")
    full, short = m.get_name("https://github.com/google-research/bert/tree/main", "code")
    assert full == "google-research/bert"
    assert short == "bert"

def test_get_name_model_basic():
    m = Model("", "", "")
    full, short = m.get_name("https://huggingface.co/google-bert/bert-base-uncased", "model")
    assert full == "google-bert/bert-base-uncased"
    assert short == "bert-base-uncased"

def test_get_name_dataset_hf():
    m = Model("", "", "")
    full, short = m.get_name("https://huggingface.co/datasets/bookcorpus/bookcorpus", "dataset")
    assert full == "bookcorpus/bookcorpus"
    assert short == "bookcorpus"

def test_get_name_dataset_external():
    m = Model("", "", "")
    full, short = m.get_name("https://example.com/dataset.zip", "dataset")
    assert full == "dataset.zip"
    assert short == "dataset.zip"

# Model.fetch_readme tests
@patch("model.requests.get")
def test_fetch_readme_github(mock_get):
    mock_get.return_value.text = "README content"
    m = Model("https://github.com/google/bert/tree/main", "", "")
    text = m.fetch_readme("code")
    assert "README content" in text

@patch("model.requests.get")
def test_fetch_readme_external(mock_get):
    m = Model("https://example.com/code", "", "")
    text = m.fetch_readme("code")
    assert text == "External" or text == ""

# Model.kw_check tests
def test_kw_check_true():
    m = Model("", "", "")
    with patch.object(m, "fetch_readme", return_value="this README mentions accuracy"):
        assert m.kw_check(["accuracy"], "code") is True

def test_kw_check_false():
    m = Model("", "", "")
    with patch.object(m, "fetch_readme", return_value="no keywords here"):
        assert m.kw_check(["accuracy"], "code") is False

# Metrics.run tests
@patch("model.HfApi.model_info")
@patch.object(Model, "get_contrib", return_value=5)
@patch.object(Model, "get_downloads", return_value=1000)
@patch.object(Model, "last_modified", return_value=True)
@patch.object(Model, "get_git_stats", return_value={"stars": 10, "forks": 2})
def test_metrics_run_basic(mock_git_stats, mock_last_modified, mock_downloads, mock_contrib, mock_info):
    mock_info.return_value = MagicMock()
    inputs = {
        "code_url": "https://github.com/google/bert",
        "dataset_url": "https://huggingface.co/datasets/bookcorpus/bookcorpus",
        "model_url": "https://huggingface.co/google-bert/bert-base-uncased"
    }
    metrics = Metrics(inputs)
    result = metrics.run()
    required_keys = [
        "name", "category", "net_score", "net_score_latency",
        "ramp_up_time", "ramp_up_time_latency", "bus_factor", "bus_factor_latency",
        "performance_claims", "performance_claims_latency", "license", "license_latency",
        "size_score", "size_score_latency", "dataset_and_code_score",
        "dataset_and_code_score_latency", "dataset_quality", "dataset_quality_latency",
        "code_quality", "code_quality_latency"
    ]
    for key in required_keys:
        assert key in result

# Metrics helper methods
def test_ms_helper():
    metrics = Metrics({"code_url": "", "dataset_url": "", "model_url": ""})
    assert isinstance(metrics._ms(1.234), int)

# Model last_modified tests
def test_last_modified_hf_false():
    m = Model("", "", "")
    m.metadata = None
    assert m.last_modified("huggingface", 30) is False

def test_last_modified_github_false():
    m = Model("https://github.com/google/bert/tree/main", "", "")
    with patch("model.requests.get") as mock_get:
        mock_get.return_value.status_code = 404
        assert m.last_modified("github", 30) is False

# Model.get_license tests
def test_get_license_unknown():
    m = Model("https://github.com/google/bert/tree/main", "", "")
    assert m.get_license() == "Unknown"

# Model.get_size tests
def test_get_size_empty_metadata():
    m = Model("", "", "https://huggingface.co/google-bert/bert-base-uncased")
    m.metadata = MagicMock(siblings=[])
    size = m.get_size()
    assert size == 0.0

# Model.get_downloads tests
def test_get_downloads_zero():
    m = Model("", "", "")
    m.metadata = None
    assert m.get_downloads() == 0

# Model.get_contrib tests
def test_get_contrib_zero():
    m = Model("", "", "")
    assert m.get_contrib() == 0

# Model.get_git_stats tests
def test_get_git_stats_empty():
    m = Model("", "","")
    m.code_url = "https://github.com/google/bert/tree/main"
    with patch("model.requests.get") as mock_get:
        mock_get.return_value.status_code = 404
        stats = m.get_git_stats()
        assert stats == {"stars": 0, "forks": 0}

# Model.add_dataset tests
def test_add_dataset_once():
    m = Model("", "", "")
    m.add_dataset("url1")
    assert "url1" in m.datasets
    m.add_dataset("url1")
    assert m.datasets.count("url1") == 1

# Model.len_readme tests
def test_len_readme_zero():
    m = Model("", "", "")
    assert m.len_readme("code") == 0


def test_add_dataset_empty_url():
    m = Model("", "", "")
    initial_len = len(m.datasets)
    m.add_dataset("")  # empty string should not be added
    assert len(m.datasets) == initial_len