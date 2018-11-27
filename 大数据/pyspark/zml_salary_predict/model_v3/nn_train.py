# -*- coding: utf-8 -*-

from .data_utils import custom_dataset
from torch.utils.data import DataLoader
from torch import nn
import torch
from torch.autograd import Variable
import math
import time
from .nn_model import NNModel
from torch.nn import init

if __name__ == '__main__':
    batch_size = 16384
    train_datas = custom_dataset('./train_data.csv')
    train_datas_loader = DataLoader(train_datas, batch_size=batch_size, shuffle=True)

    # 定义模型
    model = NNModel(2865, 1000, 100, 10, 1)

    for layer in model.modules():
        if isinstance(layer, nn.Linear):
            init.xavier_uniform_(layer.weight)

        # 定义优化器
    optimizer = torch.optim.Adam(model.parameters(), 0.001)

    # 损失函数
    criterion = nn.MSELoss()

    for i in range(100):
        train_count = 0
        batchs = 0
        for features, target in train_datas_loader:
            batchs += 1
            total_size = train_datas_loader.dataset.__len__()
            features = Variable(features)
            target = Variable(target)
            # 前向传播
            out = model(features)
            loss = criterion(out.squeeze(1), target)
            # 反向传播
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            # 记录误差
            print(
                'epoch: {} , Train Loss: {:.6f} , Mean: {:.2f} , Min: {:.2f} , Max: {:.2f} , Median: {:.2f} , Dealed/Records: {}/{} , Time: {}'. \
                    format(i, loss, math.e ** float(out.mean()),
                           math.e ** float(out.min()), math.e ** float(out.max()), math.e ** float(out.median()),
                           batchs * batch_size, total_size,
                           time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time()))))
            if batchs * batch_size > total_size:
                torch.save(model, 'model.ckpt')
