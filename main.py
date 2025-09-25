from model import Model

# Main
def main():
    """Testing functionally/example of how to use model, make sure to delete before turning it in
    m = Model(
    code_url="https://github.com/google-research/bert",
    dataset_url="https://huggingface.co/datasets/bookcorpus/bookcorpus",
    model_url="https://huggingface.co/google-bert/bert-base-uncased"
    )

    m.fetch_metadata()
    print("Model:", m.model_dict.get("name"))
    print("Code:", m.code_dict.get("name"))
    print("Dataset:", m.dataset_dict.get("name"))
    print("License:", m.get_license())
    print("Size (GB):", m.get_size())
    print("Has perf claims:", m.kw_check(["accuracy", "benchmark"], "model"))
    print("Datasets:", m.datasets)
    print("Length Code README: ", m.len_readme("code"))
    print("Length Dataset README: ", m.len_readme("dataset"))
    print("Length Model README: ", m.len_readme("model"))
    """

if __name__ == "__main__":
    main()
