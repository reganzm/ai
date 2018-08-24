import tensorflow as tf
from tensorflow.contrib import rnn
class BILSTMModel(object):
    def __init__(self, config):
        self.config = config
        # tf Graph input
        # [None, n_steps, n_input]这个None表示这一维不确定大小
        self.x = tf.placeholder(tf.int32, [None, self.config.seq_length],name='input_x')
        self.y = tf.placeholder(tf.float32, [None, self.config.num_classes],name='input_y')
        self.keep_prob = tf.placeholder(tf.float32, name='keep_prob')
        self.global_step  = tf.Variable(0, trainable=False)
        self.learning_rate = tf.train.exponential_decay(self.config.learning_rate, self.global_step, 50, 0.92, staircase=True)
        # Define weights
        self.weights = {
            # Hidden layer weights => 2*n_hidden because of forward + backward cells
            'out': tf.Variable(tf.random_normal([2*self.config.n_hidden, self.config.num_classes]))
        }
        self.biases = {
            'out': tf.Variable(tf.random_normal([self.config.num_classes]))
        }
        
        self.lstm() 
    def lstm(self):
        """BILSTM模型"""
        # 词向量映射
        with tf.device('/cpu:0'):
            embedding = tf.get_variable('embedding', [self.config.vocab_size, self.config.embedding_dim])
            embedding_inputs = tf.nn.embedding_lookup(embedding, self.x)
            #embedding_inputs = tf.contrib.layers.dropout(embedding_inputs,self.keep_prob)
        with tf.name_scope("bilstm"):
            # Prepare data shape to match `bidirectional_rnn` function requirements
            # Current data input shape: (batch_size, n_steps, n_input)
            # Required shape: 'n_steps' tensors list of shape (batch_size, n_input)
        
            # Unstack to get a list of 'n_steps' tensors of shape (batch_size, n_input)
            # 变成了n_steps*(batch_size, n_input)  
            #沿着某个维度拆分我多少份
            x = tf.unstack(embedding_inputs, self.config.n_steps, 1)
            # Define lstm cells with tensorflow
            # Forward direction cell
            lstm_fw_cell = rnn.BasicLSTMCell(self.config.n_hidden, forget_bias=1.0)
            # Backward direction cell
            lstm_bw_cell = rnn.BasicLSTMCell(self.config.n_hidden, forget_bias=1.0)
        
            # Get lstm cell output
            try:
                outputs, _, _ = rnn.static_bidirectional_rnn(lstm_fw_cell, lstm_bw_cell, x, dtype=tf.float32)
            except Exception: # Old TensorFlow version only returns outputs not states
                outputs = rnn.static_bidirectional_rnn(lstm_fw_cell, lstm_bw_cell, x,dtype=tf.float32)
        
            self.pred = tf.matmul(outputs[-1], self.weights['out']) + self.biases['out']    
            self.pred_label = tf.argmax(self.pred, 1)  

        with tf.name_scope("loss"):
            self.loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=self.pred, labels=self.y))

        with tf.name_scope("optimize"):
            self.optimizer = tf.train.AdamOptimizer(learning_rate=self.config.learning_rate).minimize(self.loss)
                   

        with tf.name_scope("accuracy"):
            # 准确率
            self.correct_pred = tf.equal(tf.argmax(self.pred,1), tf.argmax(self.y,1))
            self.accuracy = tf.reduce_mean(tf.cast(self.correct_pred, tf.float32))            