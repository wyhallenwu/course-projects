# README
my modification  
- [x] add naive data augmentation
- [x] mix-up data augmentation
- [x] cross validation

## reference
1. mix-up original paper: <https://arxiv.org/pdf/1710.09412.pdf>  
2. the auther's explanation of mix-up on Zhihu: <https://www.zhihu.com/question/67472285>  
3. cross validation: <https://www.cs.cmu.edu/~schneide/tut5/node42.html>  
   
## result
the course given baseline is: 0.50099  
my best result on validation is: 0.93292(detailed hyperparameter settings are in config.yml)  

### visualize
loss and accuracy of both training and testing with smoothing 0.6  
detailed training log is in log.txt  

1. loss of each step  
![loss](/imgs/loss.png)  

2. acc of each step  
![acc](/imgs/acc.png)

3. average loss of each epoch  
![avg loss](/imgs/avgLoss.png)

4. average acc of each epoch   
![avg acc](/imgs/avgAcc.png)