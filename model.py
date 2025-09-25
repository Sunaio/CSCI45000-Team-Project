import requests
import re
from typing import Optional, Dict
from huggingface_hub import HfApi, ModelInfo
from strip import strip_html, strip_markdown

class Model:
    def __init__(self, code_url: str, dataset_url:str , model_url:str):
        self.code_url: str = code_url
        self.dataset_url: str = dataset_url
        self.model_url: str = model_url
        self.model_name: str = self.get_name(model_url, "model")

        self.file_size_types: tuple[str, ...] = (".bin", ".safetensors")
        self.metadata: Optional[ModelInfo] = None
        self.api = HfApi()

        self.code_dict: Dict[str, str] = {"name": self.get_name(code_url, "code"), "url": self.code_url, "type": "code"}
        self.dataset_dict: Dict[str, str] = {"name": self.get_name(dataset_url, "dataset"), "url": self.dataset_url, "type": "dataset"}
        self.model_dict: Dict[str, str] = {"name": self.model_name, "url": self.model_url, "type": "model"}

        self.datasets: list[str] = []
        if dataset_url:
            self.add_dataset(dataset_url)

    # Extract name from URL
    def get_name(self, url: str, type: str) -> str:
        if not url:
            return ""

        url = url.rstrip("/")

        if type == "code":
            return url.split("github.com/")[-1].replace("tree/main", "").strip("/")
        elif type == "model":
            return url.split("huggingface.co/")[-1].replace("tree/main", "").strip("/")
        elif type == "dataset":
            if "huggingface.co" in url:
                return url.split("huggingface.co/datasets")[-1].replace("tree/main", "").strip("/")
            else:
                return url.split("/")[-1]

        return "unknown"

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

        if url_type in ["model", "dataset"] and "huggingface.co" in url:
            if self.metadata and getattr(self.metadata, "cardData", None):
                readme_text = self.metadata.cardData.get("readme", "")
                if readme_text:
                    # Strip HTML/Markdown
                    clean_text = strip_html(readme_text)
                    clean_text = strip_markdown(clean_text)
                    return clean_text
        
        if "github.com" in url:
            readme_url = url.replace("tree/main", "raw/main/README.md")
        else:
            # External dataset / other sites
            readme_url = url

        try:
            res = requests.get(readme_url, timeout=10)
            readme_text = res.text
            clean_text = strip_html(readme_text)
            clean_text = strip_markdown(clean_text)
            return clean_text
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
    
    # Number of words in README
    def len_readme(self, readme_type: str) -> int:
        text = self.fetch_readme(readme_type)
        if not text:
            return 0
        
        return len(text.split())

    # Add dataset url to list for tracking
    def add_dataset(self, dataset_url: str) -> None:
        if dataset_url and dataset_url not in self.datasets:
            self.datasets.append(dataset_url)