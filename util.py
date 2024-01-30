import os, sys


# create an empty yaml file used for yolo training
def create_yaml(path):
    with open(os.path.join(path, "dataset.yaml"), "w") as f:
        f.write(
            f"# Train/Val/Test paths\npath: {path}\ntrain: images/train\nval: images/val\n# test: (optional)\n\n# Classes\nnames:"
        )
