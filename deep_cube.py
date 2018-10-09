import argparse
import numpy as np
import sys
import time
import pdb
from cube import Cube
import torch
import torch.optim as optim
import torch.nn as nn
import torch.nn.functional as F
from torch.distributions import Categorical

class DeepCube(nn.Module):
    def __init__(self, n_in):
        super(DeepCube, self).__init__()
        self.n_in = n_in
        self.fc1 = nn.Linear(n_in, 4096)
        self.fc2 = nn.Linear(4096, 2048)
        self.pol_fc = nn.Linear(2048, 12)
        self.val_fc = nn.Linear(2048, 1)
        self._init_weights()

    def forward(self, state):
        emb = F.elu(self.fc2(F.elu(self.fc1(state))))
        pol_output = self.pol_fc(emb)
        val_output = self.val_fc(emb)
        return pol_output, val_output

    def _init_weights(self):
        for param in [self.fc1, self.fc2, self.pol_fc, self.val_fc]:
            nn.init.xavier_normal_(param.weight.data)
            param.bias.data.fill_(0)

def test(config):
    env = Cube(config.size)
    obs = env.reset()
    model = DeepCube(len(obs))
    opt = optim.Adam(model.parameters(), lr=config.lr)

    mseloss = nn.MSELoss()
    celoss = nn.CrossEntropyLoss()

    start = time.time()
    pol_preds = []
    pol_targets = []
    val_preds = []
    val_targets = []

    for i in range(config.episodes):
        torch_obs = torch.Tensor(obs)
        pred_pol, pred_val = model(torch_obs)
        nxt_cubes = env.next_states()
        next_states = np.stack([c.onehot_state() for c in nxt_cubes])
        next_rews = np.array([1 if c.solved() else -1 for c in nxt_cubes])
        tnxt = torch.Tensor(next_states)
        nxt_pols, nxt_vals = model(tnxt)

        target_val, target_idx = torch.max(torch.Tensor(next_rews).unsqueeze(-1) + nxt_vals, dim=0)
        target_action = torch.zeros(6)
        target_action[target_idx] = 1
        pol_preds.append(pred_pol)
        val_preds.append(pred_val)
        val_targets.append(target_val)
        pol_targets.append(target_idx)

        if i % config.batch_size:
            t_pol_pred = torch.stack(pol_preds)
            t_pol_targets = torch.stack(pol_targets)
            t_val_pred = torch.stack(val_preds)
            t_val_targets = torch.stack(val_targets).detach()
            opt.zero_grad()
            loss = mseloss(t_val_pred, t_val_targets) + celoss(t_pol_pred, t_pol_targets.squeeze(-1))
            loss.backward()
            opt.step()

            pol_preds = []
            pol_targets = []
            val_preds = []
            val_targets = []

        if i % 10 == 0:
            print("Epoch {}".format(i))
        action = target_idx.item()
        new_obs, reward, done, _ = env.step(action)
        obs = new_obs

    elapsed = time.time() - start
    print('Time for {} steps | {:.2f}'.format(steps, elapsed))

def get_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('--size', type=int, default=3)
    parser.add_argument('--batch_size', type=int, default=100)
    parser.add_argument('--episodes', type=int, default=10000)
    parser.add_argument('--lr', type=float, default=1e-3)
    return parser.parse_args()

if __name__ == '__main__':
    config = get_config()
    test(config)
