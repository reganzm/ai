# -*- coding: utf-8 -*-
from torch import nn


class NNModel(nn.Module):
    def __init__(self, num_input, num_hidden1, num_hidden2, num_hidden3, output):
        super(NNModel, self).__init__()
        self.layer1 = nn.Linear(num_input, num_hidden1, bias=True)
        self.active1 = nn.ReLU()
        # self.drop_out1 = nn.Dropout(p=0.7)
        self.layer2 = nn.Linear(num_hidden1, num_hidden2, bias=True)
        self.active2 = nn.ReLU()
        # self.drop_out2 = nn.Dropout(p=0.8)
        self.layer3 = nn.Linear(num_hidden2, num_hidden3, bias=True)
        self.active3 = nn.ReLU()
        # self.drop_out3 = nn.Dropout(p=0.9)
        self.out = nn.Linear(num_hidden3, output, bias=True)

    def forward(self, x):
        # 第一层
        x = self.layer1(x)
        x = self.active1(x)
        # x = self.drop_out1(x)
        # 第二层
        x = self.layer2(x)
        x = self.active2(x)
        # x = self.drop_out2(x)
        # 第三层
        x = self.layer3(x)
        x = self.active3(x)
        # x = self.drop_out3(x)
        # 输出层
        x = self.out(x)
        return x
