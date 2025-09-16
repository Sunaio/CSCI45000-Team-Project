"""Handles all data fetching."""
class Model:
    def __init__(self, url: str) -> None:
       self.url: str = url
       self.name: str = self.get_name(url)
       self.category: str = "Model"

       self.github_url: str = "placeholder"
       
    """Gets model name from URL"""
    def get_name(self, url: str) -> str:
       return url.strip("/").split("/")[-1]
    

