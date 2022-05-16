condition: mixup, train
if mixup and train:
    test_tfm + mixup
if test:
    test_tfm
if train:
    train_tfm

batch_size, 11
labels batch_size, 2