from model import Model

# Use main for testing currently
def main():
    """
    model_url = "https://huggingface.co/Qwen/Qwen3-Next-80B-A3B-Thinking"
    
    # Create model instance
    model = Model(model_url)
    
    print(f"Model name: {model.name}")
    print(f"Model category: {model.category}")
    
    # Fetch Hugging Face metadata
    print("\nFetching Hugging Face metadata...")
    model.fetch_huggingface_metadata()
    print("HF Metadata:")
    
    # Fetch repository data (README, license)
    print("\nFetching repository data...")
    model.fetch_repo_data()

    print("Author:", model.hf_metadata.get("author", "Unknown"))
    print("Downloads:", model.hf_metadata.get("downloads", 0))
    print("Likes", model.hf_metadata.get("likes", 0))
    print("Pipeline tag:", model.hf_metadata.get("pipeline_tag", "Unknown"))
    print("License:", model.repo_data.get("license", "unknown"))
    """

if __name__ == "__main__":
    main()
