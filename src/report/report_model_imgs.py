import torch
import cv2

from report_model_comparison import runs
from src.dataset import data_path, StereopsisDataset
from src.models.dispnet import NNModel
from src.net_tester import tester

logs = {r: data_path.joinpath(f"logs/{runs[r]}") for r in runs}

epochs = 200
current_device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
img_path = data_path.joinpath("processed/report-imgs/")

for i, run in enumerate(logs):
    model = NNModel(batch_norm=True)
    model_weights = torch.load(logs[run].joinpath(f"model-e{epochs}.pt"), map_location=current_device)
    model.load_state_dict(model_weights)

    ds = StereopsisDataset(img_dir=img_path.joinpath(str(i)), val_split_ratio=1.0)

    results = tester(model, ds, run, None, False)
    for key in results.keys():
        pred = results[key]["pred"].squeeze().numpy()
        cv2.imwrite(img_path.joinpath("preds_by_disp", str(i), f"pred_{key}.tiff").as_posix(), pred)