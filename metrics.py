# metrics.py
from __future__ import annotations

import time
from typing import Dict

from model import Model


# --- thresholds & keywords ---
CODE_README_OK_WORDS = 100
BUS_FACTOR_WORDS = 300
DATASET_README_OK_WORDS = 100

PERF_KWS = ["accuracy", "benchmark", "state-of-the-art", "sota", "f1", "bleu", "rouge", "perplexity"]
DATASET_KWS = ["license", "download", "split", "train", "test", "validation"]

SIZE_THRESHOLDS_GB: Dict[str, float] = {
    "raspberry_pi": 0.5,
    "jetson_nano": 1.0,
    "desktop_pc": 6.0,
    "aws_server": 15.0,
}


def _ms(seconds: float) -> int:
    return int(round(seconds * 1000.0))


def compute_metrics(m: Model) -> Dict[str, object]:
    """
    Compute all required metrics using only model.py methods.
    All scores are 0 or 1. Latencies are ints in milliseconds.
    """

    # --- metadata ---
    t0 = time.time()
    m.fetch_metadata()
    metadata_latency = _ms(time.time() - t0)
    hf_ok = m.metadata is not None

    # --- license ---
    t0 = time.time()
    license_str = m.get_license() if hf_ok else "Unknown"
    license_latency = _ms(time.time() - t0)
    license_score = 1.0 if (license_str and license_str.lower() != "unknown") else 0.0

    # --- size_score ---
    t0 = time.time()
    size_gb = m.get_size() if hf_ok else 0.0
    size_latency = _ms(time.time() - t0)
    size_score = {
        dev: (1.0 if (size_gb > 0.0 and size_gb <= limit) else 0.0)
        for dev, limit in SIZE_THRESHOLDS_GB.items()
    }

    # --- ramp_up_time (code README) ---
    t0 = time.time()
    code_words = m.len_readme("code")
    ramp_latency = _ms(time.time() - t0)
    ramp_up_time = 1.0 if code_words >= CODE_README_OK_WORDS else 0.0

    # --- bus_factor ---
    bus_latency = ramp_latency  # reuse
    bus_factor = 1.0 if code_words >= BUS_FACTOR_WORDS else 0.0

    # --- performance_claims ---
    t0 = time.time()
    perf_claims = 1.0 if m.kw_check(PERF_KWS, "model") else 0.0
    perf_latency = _ms(time.time() - t0)

    # --- dataset_quality ---
    t0 = time.time()
    ds_words = m.len_readme("dataset")
    ds_kws = m.kw_check(DATASET_KWS, "dataset")
    ds_quality = 1.0 if (ds_words >= DATASET_README_OK_WORDS and ds_kws) else 0.0
    ds_latency = _ms(time.time() - t0)

    # --- dataset_and_code_score ---
    t0 = time.time()
    has_code = bool(m.code_dict.get("url"))
    has_ds = bool(m.dataset_dict.get("url"))
    ds_code_score = 1.0 if (has_code and has_ds and code_words > 0 and ds_words > 0) else 0.0
    ds_code_latency = _ms(time.time() - t0) + ramp_latency + ds_latency

    # --- availability_score ---
    t0 = time.time()
    availability = 1.0 if (hf_ok or code_words > 0 or ds_words > 0) else 0.0
    avail_latency = _ms(time.time() - t0) + metadata_latency

    # --- net_score (strict AND) ---
    core = [
        license_score,
        max(size_score.values() or [0.0]),
        ramp_up_time,
        bus_factor,
        availability,
    ]
    net_score = 1.0 if all(v == 1.0 for v in core) else 0.0
    net_latency = license_latency + size_latency + ramp_latency + bus_latency + avail_latency

    return {
        "name": m.model_dict.get("name") or m.dataset_dict.get("name") or m.code_dict.get("name") or "unknown",
        "category": "MODEL",
        "net_score": float(net_score),
        "net_score_latency": int(net_latency),

        "ramp_up_time": float(ramp_up_time),
        "ramp_up_time_latency": int(ramp_latency),

        "bus_factor": float(bus_factor),
        "bus_factor_latency": int(bus_latency),

        "performance_claims": float(perf_claims),
        "performance_claims_latency": int(perf_latency),

        "license": float(license_score),
        "license_latency": int(license_latency),

        "size_score": {k: float(v) for k, v in size_score.items()},
        "size_score_latency": int(size_latency),

        "dataset_and_code_score": float(ds_code_score),
        "dataset_and_code_score_latency": int(ds_code_latency),

        "dataset_quality": float(ds_quality),
        "dataset_quality_latency": int(ds_latency),

        "availability_score": float(availability),
        "availability_score_latency": int(avail_latency),
    }
