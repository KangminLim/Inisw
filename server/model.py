import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import numpy as np
import random
from torch.utils.data import Dataset, DataLoader, random_split
import torch.optim as optim


class proj_head(nn.Module):
  def __init__(self):
    super().__init__()
    self.vid = nn.Sequential(
        nn.Linear(2048, 1024, bias=True),
        nn.BatchNorm1d(1024),
        nn.ReLU(),
        nn.Linear(1024, 512, bias=True),
        nn.BatchNorm1d(512),
    )
    self.aud = nn.Linear(2048, 512, bias=True)
    self.tex = nn.Sequential(
        nn.Linear(2048, 512, bias=True),
        nn.ReLU()
    )
  def forward(self, x, y, z):
    x1 = self.vid(x)
    y1 = self.aud(y)
    z1 = self.tex(z)
    return x1, y1, z1
  
class NCELoss(nn.Module):
    def __init__(self ,temperature=0.07):
        super(NCELoss, self).__init__()
        self.temperature = temperature

    def forward(self, v_f, a_f, t_f):
        v_f = F.normalize(v_f, dim=-1)
        a_f = F.normalize(a_f, dim=-1)
        t_f = F.normalize(t_f, dim=-1)
        possim1 = []
        negsim1 = []
        NCE = []
        start_index = 0

        # Pos, neg pair 만들기
        for i in range(v_f.size(0)):
            possim = torch.matmul(v_f[i], a_f[i])
            possim1.append(possim)
            for j in range(v_f.size(0)):
                if i != j:
                    negsim = torch.matmul(v_f[i], a_f[j])
                    negsim1.append(negsim)

        # NCELoss 계산
        for k in range(v_f.size(0)):
            sumexp_all = 0
            sumexp_neg = 0
            end_index = start_index + v_f.size(0)
            exp_pos = torch.exp(possim1[k] / self.temperature)

            for l in range(end_index):
                sumexp_neg += torch.exp(negsim1[l] / self.temperature)
            sumexp_all = exp_pos + sumexp_neg
            loss = torch.log(sumexp_all) - torch.log(exp_pos)
            NCE.append(loss)


        possim_vt1 = []
        negsim_vt1 = []
        NCE_vt = []
        start_index_vt = 0

        # Pos, neg pair 만들기
        for i in range(v_f.size(0)):
            possim_vt = torch.matmul(v_f[i], t_f[i])
            possim_vt1.append(possim_vt)
            for j in range(v_f.size(0)):
                if i != j:
                    negsim_vt = torch.matmul(v_f[i], t_f[j])
                    negsim_vt1.append(negsim_vt)

        # NCELoss 계산
        for k in range(v_f.size(0)):
            sumexp_all_vt = 0
            sumexp_neg_vt = 0
            end_index_vt = start_index_vt + v_f.size(0)
            exp_pos_vt = torch.exp(possim_vt1[k] / self.temperature)

            for l in range(end_index_vt):
                sumexp_neg_vt += torch.exp(negsim_vt1[l] / self.temperature)
            sumexp_all_vt = exp_pos_vt + sumexp_neg_vt
            loss_vt = torch.log(sumexp_all_vt) - torch.log(exp_pos_vt)
            NCE_vt.append(loss_vt)
        # list -> tensor화
        NCE = torch.stack(NCE)
        NCE_vt = torch.stack(NCE_vt)
        # None값 제거
        NCE = torch.where(torch.isnan(NCE), torch.zeros_like(NCE), NCE)
        NCE_vt = torch.where(torch.isnan(NCE_vt), torch.zeros_like(NCE_vt), NCE_vt)

        loss = torch.mean(NCE)
        loss_vt = torch.mean(NCE_vt)
        return loss, loss_vt


