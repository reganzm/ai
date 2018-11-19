# -*- coding: utf-8 -*-

from .data_utils import custom_dataset
from torch.utils.data import DataLoader
from torch import nn
import torch
from torch.autograd import Variable
import math
import time
from .nn_model import NNModel

if __name__ == '__main__':
    train_type = 'min'
    batch_size = 4096
    train_datas = custom_dataset('./shuffled_train_datas.csv', train_type=train_type)
    train_datas_loader = DataLoader(train_datas, batch_size=batch_size, shuffle=True)

    test_datas = custom_dataset('./shuffled_test_datas.csv', train_type=train_type)
    test_datas_loader = DataLoader(test_datas, batch_size=batch_size, shuffle=True)

    # 定义模型
    model = NNModel(4353, 1000, 100, 10, 1)

    # 定义优化器
    optimizer = torch.optim.Adam(model.parameters(), 0.001)

    # 损失函数
    criterion = nn.MSELoss()


    # 参数值初始化
    def weight_init(m):
        if isinstance(m, nn.Linear):
            # m.parameters.data.fill_(1)
            m.bias.data.zero_()


    # 调用参数初始化方法初始化网络参数
    model.apply(weight_init)

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
                torch.save(model, 'model_' + train_type + '.ckpt')
