from .data_utils import custom_dataset

if __name__ == '__main__':
    datasets = custom_dataset('./train_datas.csv')
    print(next(iter(datasets)))
