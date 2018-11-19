# -*- coding: utf-8 -*-
from .data_utils import custom_dataset
from torch.utils.data import DataLoader
from torch import nn
import torch
import math
import time
import numpy as np

if __name__ == '__main__':
    train_type = 'min'
    batch_size = 10000
    test_datas = custom_dataset('./test_data.csv')
    test_datas_loader = DataLoader(test_datas, batch_size=batch_size, shuffle=True)

    # 读取模型
    model_path = 'model.ckpt'
    model = torch.load(model_path)
    # 转化为测试模式
    model.eval()
    # 损失函数
    criterion = nn.MSELoss()
    results = []
    targets = []
    batchs = 0
    for features, target in test_datas_loader:
        batchs += 1
        total_size = test_datas_loader.dataset.__len__()
        # 前向传播
        out = model(features)
        results.append([math.e ** float(i) for i in out])
        targets.append([math.e ** float(i) for i in target])
        loss = criterion(out.squeeze(1), target)
        print(
            'Test Loss: {:.6f} , Mean: {:.2f} , Min: {:.2f} , Max: {:.2f} , Median: {:.2f} , Dealed/Records: {}/{} , Time: {}'. \
            format(loss, math.e ** float(out.mean()),
                   math.e ** float(out.min()), math.e ** float(out.max()), math.e ** float(out.median()),
                   batchs * batch_size, total_size, time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time()))))
    result_map = {'out': results, 'target': targets}
    np.save('result_map', result_map)
