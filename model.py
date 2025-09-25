import requests
import re
from typing import Optional
from huggingface_hub import HfApi, ModelInfo

class Model:
    def __init__(self, code_url: str, dataset_url:str , model_url:str):
        self.code_url: str = code_url
        self.dataset_url: str = dataset_url
        self.model_url: str = model_url
        self.model_name: str = self.get_model_name(self.model_url)
        self.category: str
        self.file_size_types: tuple[str, ...] = (".bin", ".safetensors")
        self.metadata: Optional[ModelInfo] = None
        self.api = HfApi()
        self.datasets: list[str] = []
        
        if dataset_url:
            self.add_dataset(dataset_url)

    # Model Name
    def get_model_name(self, url: str) -> str:
        model_name = self.model_url.split("huggingface.co/")[-1].replace("tree/main", "").strip("/")
        return model_name

    # HF API fetch
    def fetch_metadata(self) -> None:
        try:
            self.metadata = self.api.model_info(self.model_name)
        except Exception as e:
            print(f"Error fetching metadata for {self.model_name}: {e}")
            self.metadata = None

    # README raw text data
    def fetch_readme(self, url_type: str) -> str:
        readme_text = ""
        readme_url = ""

        url_map = {
            "code": self.code_url,
            "dataset": self.dataset_url,
            "model": self.model_url,
        }

        url = url_map.get(url_type)
        if not url:
            return ""

        readme_url = url.replace("tree/main", "raw/main/README.md")
        
        try:
            res = requests.get(readme_url, timeout=10)
            readme_text = res.text if res.status_code == 200 else ""
            return readme_text
        except Exception as e:
            print("Error fetching readme {e}")
            return ""

    # Model licenses
    def get_license(self) -> str:
        card_data = getattr(self.metadata, "cardData", None)
        if card_data:
            license_name = card_data.get("license_name") or card_data.get("license")
            if license_name:
                return license_name
        return "Unknown"

    # Size of model
    def get_size(self) -> float:
        total_bytes = 0
        for f in getattr(self.metadata, "siblings", []):
            filename = getattr(f, "rfilename", "")
            if filename.endswith(self.file_size_types):
                file_url = f"{self.model_url}/resolve/main/{filename}"
                try:
                    res = requests.head(file_url, timeout=15, allow_redirects=True)
                    size = int(res.headers.get("Content-Length", 0) or 0)
                    total_bytes += size
                except Exception as e:
                    print(f"Error fetching size for {filename}: {e}")
        return total_bytes / (1024**3)

    # Check README for keywords
    def kw_check(self, kw: list[str], readme_type: str) -> bool:
        text = self.fetch_readme(readme_type).lower()
        if not text.strip():
            return False
        for k in kw:
            word = r"\b" + re.escape(k.lower()) + r"\b"
            if re.search(word, text):
                return True
        return False

    # Add dataset url to list for tracking
    def add_dataset(self, dataset_url: str) -> None:
        if dataset_url and dataset_url not in self.datasets:
            self.datasets.append(dataset_url)