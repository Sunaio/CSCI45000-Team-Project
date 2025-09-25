from model import Model

def main():
    m = Model(
    code_url="https://github.com/google-research/bert",
    dataset_url="https://huggingface.co/datasets/bookcorpus/bookcorpus",
    model_url="https://huggingface.co/google-bert/bert-base-uncased"
    )

    m.fetch_metadata()
    print("Model:", m.model_name)
    print("License:", m.get_license())
    print("Size (GB):", m.get_size())
    print("Has perf claims:", m.kw_check(["accuracy", "benchmark"], "model"))
    print("Datasets:", m.datasets)

if __name__ == "__main__":
    main()
