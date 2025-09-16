import requests
from typing import Dict, Any, List

# Testing


# Handles all data fetching
class Model:
    def __init__(self, url: str) -> None:
       self.url: str = url
       self.name: str = self.get_name(url)
       self.category: str = "Model"

       # Data containers for fetched data
       # hf_metadata includes downloads, like, author, etc
       # repo_data includes readme raw text and license
       self.hf_metadata: Dict[str, Any] = {}
       self.repo_data: Dict[str, Any] = {}

    # Gets model name from URL
    def get_name(self, url: str) -> str:
       return url.strip("/").split("/")[-1]
    
    # Fetch metadata from huggingface URL
    def fetch_huggingface_metadata(self) -> None:
       try:
        part: str = (
           self.url.split("huggingface.co/")[-1]
           .replace("tree/main", "")
           .strip("/")
        )
        
        api_url: str = f"https://huggingface.co/api/models/{part}"
        
        # Tries to request to api url
        res = requests.get(api_url, timeout = 10)

        # If connect succeeds, parse the JSON response into the dictionary
        if res.status_code == 200:
            self.hf_metadata = res.json()
        else:
            self.hf_metadata = {}

       except Exception as e:
          print("Error: {e}")
    
    def fetch_repo_data(self) -> None:
        try:
            # Fetch README
            readme_url: str = self.url.replace(
                "tree/main", "raw/main/README.md"
            )

            res = requests.get(readme_url, timeout=10)
            self.repo_data["readme"] = (
                res.text if res.status_code == 200 else ""
            )

            # License
            license_method = self.hf_metadata.get("license") or \
                self.hf_metadata.get("cardData", {}).get("license_name") or \
                self.hf_metadata.get("cardData", {}).get("license") or \
                "Unknown"
            self.repo_data["license"] = license_method

        except Exception as e:
            print("Error: {e}")
            self.repo_data = {}