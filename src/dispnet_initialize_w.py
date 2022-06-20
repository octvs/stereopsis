import torch
from dataset import data_path
from models import dispnet
import pickle


def create_txt_to_compare(src_weights, net):
    dispnet_keys = list(src_weights.keys())[4:]
    my_dict = net.state_dict()
    my_keys = list(my_dict.keys())
    txt = ""
    for key0, key1 in zip(dispnet_keys, my_keys):
        same_shape = src_weights[key0].shape == my_dict[key1].shape
        if not same_shape:
            txt += f"---\n"
            txt += f"{key0}-\n{src_weights[key0].shape}\n"
            txt += f"{key1}\n{my_dict[key1].shape}\n"
            txt += f"---\n"
        else:
            txt += f"{key0}-{key1}\n"
            txt += f"{src_weights[key0].shape}\n"

    print(txt)

    with open("layer_name_conv.txt", "w") as f:
        f.write(txt)


def create_dict():
    dct = {}
    with open("layer_name_conv.txt", "r") as f:
        a = f.read().splitlines()
    for line in a:
        key0, key1 = line.split("-")
        dct[key1] = key0
    with open("../data/processed/dispnet_layer_converter.pkl", "wb") as f:
        pickle.dump(dct, f)


def ingest_weights_to_model(net):
    target_weights = torch.load(data_path.joinpath('raw/dispnet_cvpr2016.pt'))
    with open(data_path.joinpath("processed/dispnet_layer_converter.pkl"), "rb") as f:
        layer_converter = pickle.load(f)

    for name, param in net.named_parameters():
        old_layer_name = layer_converter.get(name, None)
        if not old_layer_name:
            if name.split(".")[-2] == "batch_norm":
                torch.nn.init.constant_(param.data, int(name.split(".")[-1] == "weight"))
            else:
                print(f"Unexpected layer {name}, leaving as it is!")
        else:
            param.data = target_weights[old_layer_name]


if __name__ == "__main__":
    pretrained_weights = torch.load(data_path.joinpath('raw/dispnet_cvpr2016.pt'))
    my_model = dispnet.NNModel(batch_norm=True)

    # create_txt_to_compare(target_weights, my_model)
    # Close and edit the file, be careful with refiners
    # layer_converter = create_dict()
    ingest_weights_to_model(my_model)
