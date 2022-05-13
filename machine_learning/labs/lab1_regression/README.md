# notes
the goal of this lab is to predict covid19.   
this lab helps to get familar with pytorhc.

## dataset exploration
the dataset is from [`dataset kaggle`](https://www.kaggle.com/competitions/ml2022spring-hw1/data), there are two files in the dataset: `covid.train.csv`,  `covid.test.csv`. We divide training set into trainset and validset by setting `valid_ratio` in `config.py`  
`covid.train.csv` is of shape[2699, 138] while `covid.test.csv` is [1078, 137]  
there are some features(such as states) may not help in this project. A task of this lab is to explore could it perform better if excluding these features?  

## structure
the given code is organised in a single file which is not a good code pattern. I reorganise the code by handwriting. It is helpful for beginner to go through the code and understand the pipeline.

## train
```bash
sudo python3 train.py
```

> sudo is optional because in utility.trainer needs make a directory.
