class BILSTMConfig(object):
    """BILSTM配置参数"""

    embedding_dim = 100  # 词向量维度
    seq_length = 1000  # 序列长度
    num_classes = 19  # 类别数

    vocab_size = 1271460  # 词汇表达小

    dropout_keep_prob = 0.5  # dropout保留比例
    learning_rate = 0.01  # 学习率
    
    n_input = embedding_dim
    n_steps = seq_length # timesteps
    
    # 隐藏层大小
    n_hidden = 128 # hidden layer num of features
    

    batch_size = 128  # 每批训练大小
    num_epochs = 10  # 总迭代轮次

    print_per_batch = 10  # 每多少轮输出一次结果
    save_per_batch = 10  # 每多少轮存入tensorboard