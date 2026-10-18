import numpy as np
import pandas as pd
import torch


def main() -> None:
    images = torch.randn(8, 3, 224, 224)
    logits = torch.nn.Linear(512, 10)(torch.randn(8, 512))
    features = np.random.rand(1000, 512).astype(np.float32)
    labels = np.random.randint(0, 10, size=1000)
    metrics = pd.DataFrame({"epoch": range(20), "loss": np.random.rand(20)})
    boxes = [[12, 40, 88, 120]] * 37
    name = "resnet50"
    print("inspect")


main()
