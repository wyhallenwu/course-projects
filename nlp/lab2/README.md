## readings
1. [分词1](https://easyai.tech/ai-definition/tokenization/)

## notes
文本是一些非结构化的数据，分词的目的就是将这些数据转化为结构化的数据。词是表达完整语义的最小单位，分词现在已经不一定是nlp任务的基础了[(is segmentation necessary)](https://arxiv.org/pdf/1905.05526.pdf)  
中文分词的三种基本方法：  
1. 基于词典：
   1. 正向最大匹配
   2. 逆向最大匹配
   3. 双向匹配
2. 基于统计
   1. HMM
   2. CRF
   3. SVM
3. 基于深度学习
   1. LSTM+CRF

我本次实验实现的是基于词典的MMSEG算法，MMSEG算法是正向最大匹配的扩展

## Some declarations
This repository contains my implementation of MMSEG algorithm which is a widely used Chinese segmentation algorithm. In this lab, I try Golang not Python.  
I implement it according to MMSEG official site http://technology.chtsai.org/mmseg/  
MMSEG is a simple but useful algorithm to solve Chinese segmentation problems. Although there are many new solutions for this task, but you can find them more or less influenced by MMSEG.  
## Declaration
**reference**: 
1. [kenzhengguan's implementation](https://github.com/kenzhengguan/gommseg)  
2. MMSEG official implementation and I download source code, you can check in lab2/mmseg_official_code/  
3. [more intuitive explanation of MMSEG](https://blog.csdn.net/HHyatt/article/details/6202826)