import torch
import torch.nn as nn
import cv2
import numpy as np

# SIMPLE CNN LIVENESS MODEL (lightweight production baseline)
class LivenessCNN(nn.Module):
    def __init__(self):
        super(LivenessCNN, self).__init__()

        self.model = nn.Sequential(
            nn.Conv2d(3, 16, 3, 1, 1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(16, 32, 3, 1, 1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(32, 64, 3, 1, 1),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d(1),

            nn.Flatten(),
            nn.Linear(64, 2)  # real vs fake
        )

    def forward(self, x):
        return self.model(x)


model = LivenessCNN()
model.eval()


def preprocess(frame):
    img = cv2.resize(frame, (64, 64))
    img = img / 255.0
    img = np.transpose(img, (2, 0, 1))
    img = torch.tensor(img).float().unsqueeze(0)
    return img


def is_real_face(frame):
    try:
        tensor = preprocess(frame)

        with torch.no_grad():
            output = model(tensor)
            pred = torch.argmax(output, dim=1).item()

        return pred == 1  # 1 = real, 0 = fake

    except:
        return True  # fallback (don’t block system if model fails)