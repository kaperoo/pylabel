import os, sys, yaml


# create an empty yaml file used for yolo training
def create_yaml(path):
    data = {
        "path": path,
        "train": "images/train",
        "val": "images/val",
        "test": "",
        "names": {},
    }
    yaml.dump(data, open(os.path.join(path, "dataset.yaml"), "w"), sort_keys=False)


def get_classes(path):
    data = yaml.load(open(path, "r"), Loader=yaml.FullLoader)
    return data["names"]


def add_class(path, class_name):
    data = yaml.load(open(path, "r"), Loader=yaml.FullLoader)

    if data["names"] is None:
        data["names"] = {}
        data["names"][0] = class_name

    else:
        if class_name in data["names"].values():
            return

        last_index = 0
        for i in data["names"]:
            if int(i) > last_index:
                last_index = int(i)
        data["names"][last_index + 1] = class_name

    yaml.dump(data, open(path, "w"), sort_keys=False)


def check_dir_tree(path, level=0):
    # level 0
    if not os.path.exists(path):
        os.mkdir(path)

    # level 1
    if level > 0:
        if not os.path.exists(os.path.join(path, "images")):
            os.mkdir(os.path.join(path, "images"))
        if not os.path.exists(os.path.join(path, "labels")):
            os.mkdir(os.path.join(path, "labels"))
        if not os.path.exists(os.path.join(path, "dataset.yaml")):
            create_yaml(path)

    # level 2
    if level > 1:
        if not os.path.exists(os.path.join(path, "images", "train")):
            os.mkdir(os.path.join(path, "images", "train"))
        if not os.path.exists(os.path.join(path, "images", "val")):
            os.mkdir(os.path.join(path, "images", "val"))
        if not os.path.exists(os.path.join(path, "labels", "train")):
            os.mkdir(os.path.join(path, "labels", "train"))
        if not os.path.exists(os.path.join(path, "labels", "val")):
            os.mkdir(os.path.join(path, "labels", "val"))
