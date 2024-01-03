import torch
import numpy as np
class CustomtrainDataset(torch.utils.data.Dataset):
    def __init__(self, x_file, y_file,z_file):
        self.x_data = np.load(x_file, allow_pickle=True)
        self.y_data = np.load(y_file, allow_pickle=True)
        self.z_data = np.load(z_file, allow_pickle=True)


    def __len__(self):
        return len(self.x_data)

    def __getitem__(self, idx):
        x = self.x_data[idx]
        y = self.y_data[idx]
        z = self.z_data[idx]

        z = z.squeeze(0)
        x_t = torch.from_numpy(x)
        y_t = torch.from_numpy(y)
        z_t = torch.from_numpy(z)
 

        return x_t, y_t,z_t
 