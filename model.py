import requests
import re
from typing import Optional
from huggingface_hub import HfApi, ModelInfo

class Model:
    def __init__(self, url: str):
        self.url: str = url
        self.name: str = self.get_name(url)
        self.file_size_types: tuple[str, ...] = (".bin", ".safetensors")
        self.metadata: Optional[ModelInfo] = None
        self.readme_data: str = ""
        self.api = HfApi()
        # Token is required for some HF API data
        token_input = input("Enter your Hugging Face access token: ")
        self.token = token_input

    # Returns model name
    def get_name(self, url: str) -> str:
        part = url.split("huggingface.co/")[-1].replace("tree/main", "").strip("/")
        return part

    # Fetch HF repo data
    def fetch_metadata(self) -> None:
        try:
            self.metadata = self.api.model_info(self.name, token = self.token)
        except Exception as e:
            print(f"Error fetching metadata for {self.name}: {e}")
            self.metadata = None

    # Fetch and convert README to raw text
    def fetch_readme(self) -> None:
        try:
            readme_url = self.url.replace("tree/main", "raw/main/README.md")
            res = requests.get(readme_url, timeout = 10)
            self.readme_data = res.text if res.status_code == 200 else ""
        except Exception as e:
            print(f"Error fetching README: {e}")
            self.readme_data = ""

    # Return model license
    def get_license(self) -> str:
        card_data = getattr(self.metadata, "cardData", None)
        if card_data:
            license_name = card_data.get("license_name") or card_data.get("license")
            if license_name:
                return license_name
            
        return "Unknown"

    # Return model size
    def get_size(self) -> float:
        total_bytes = 0
        if total_bytes == 0:
            headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
            for f in getattr(self.metadata, "siblings", []):
                filename = getattr(f, "rfilename", "")
                if filename.endswith(self.file_size_types):
                    file_url = f"{self.url}/resolve/main/{filename}"
                    try:
                        res = requests.head(file_url, headers=headers, timeout=15, allow_redirects=True)
                        size = int(res.headers.get("Content-Length", 0) or 0)
                        total_bytes += size
                    except Exception as e:
                        print(f"Error fetching size for {filename}: {e}")

        # Bytes -> Gb
        return total_bytes / (1024**3)
    
    # Return true if model readme has certain performance claims keywords
    def has_perf_claims(self, kw: list[str]) -> bool:
        text = self.readme_data.lower()
        if not text.strip():
            return False
        
        for k in kw:
            word = r"\b" + re.escape(k.lower()) + r"\b"
            if(re.search(word, text)):
                return True
        
        return False
    
    # Return true if model readme has certain ramp up keywords (anything that helps user get started)
    def has_ramp_up(self, kw: list[str]) -> bool:
        text = self.readme_data.lower()
        if not text.strip():
            return False
      
        for k in kw:
            word = r"\b" + re.escape(k.lower()) + r"\b"
            if(re.search(word, text)):
                return True
        
        return False