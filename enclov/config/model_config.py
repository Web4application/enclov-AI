from dataclasses import dataclass
from typing import Optional
import os
import torch
from cpufeature import CPUFeature
from petals.constants import PUBLIC_INITIAL_PEERS

@dataclass
class ModelInfo:
    repo: str
    adapter: Optional[str] = None

MODELS = [
    ModelInfo(repo="meta-llama/Llama-2-70b-chat-hf"),
    ModelInfo(repo="stabilityai/StableBeluga2"),
    ModelInfo(repo="enoch/llama-65b-hf"),
    ModelInfo(repo="enoch/llama-65b-hf", adapter="timdettmers/guanaco-65b"),
    ModelInfo(repo="bigscience/bloomz"),
]

DEFAULT_MODEL_NAME = os.getenv("MODEL_NAME", "enoch/llama-65b-hf")
INITIAL_PEERS = os.getenv("INITIAL_PEERS", "").split(",") if os.getenv("INITIAL_PEERS") else PUBLIC_INITIAL_PEERS
MAX_SESSIONS = int(os.getenv("MAX_SESSIONS", 50))
STEP_TIMEOUT = int(os.getenv("STEP_TIMEOUT", 5 * 60))

DEVICE = os.getenv("DEVICE", "cuda" if torch.cuda.is_available() else "cpu")

if DEVICE == "cuda":
    TORCH_DTYPE = "auto"
elif CPUFeature["AVX512f"] and CPUFeature["OS_AVX512"]:
    TORCH_DTYPE = torch.bfloat16
else:
    TORCH_DTYPE = torch.float32
