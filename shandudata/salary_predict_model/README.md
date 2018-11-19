###salary_predict 薪资预测(算薪资)
#### 项目版本:
##### alpha : 
[http://suanxinzi.com/](http://suanxinzi.com/)

 * 服务器提供后端(tornado)服务
 * 模型训练,offline文件夹
 *  模型训练结果,salary.model文件夹,(upper.model,lower.model)
 
##### pro :
[http://pro.suanxinzi.com/](http://pro.suanxinzi.com/)

 * web服务,web文件夹,
 > 启动服务,./run_pro_web
 
 * 模型训练,train_model文件夹
 * 模型训练结果,train_model文件夹,*.model
 
#### pro 提供的一些其他服务(后续需要重新整理独立出来)
 * 提供网址生成图片服务
 * 提供静态资源服务(markdown文档中引用到的一些图片)


#### 算薪资项目后续规划
#### 1.算法模型
kaggle上有一个关于薪资预测的竞赛,[Job salary prediction](http://www.kaggle.com/c/job-salary-prediction),比赛的内容是根据历史的招聘数据，然后预测每个测试集中每行数据对应的薪水。**衡量模型好坏的标准是MAE。**

相关文章:

* [http://fastml.com/predicting-advertised-salaries/](http://fastml.com/predicting-advertised-salaries/) (Hiton实验室,多伦多大学)

* [Q&A With Job Salary Prediction First Prize Winner Vlad Mnih](http://blog.kaggle.com/2013/05/06/qa-with-job-salary-prediction-first-prize-winner-vlad-mnih/)

* [Q&A with Vlado Boza, **2nd Place Winner**, Job Salary Prediction Competition](http://blog.kaggle.com/2013/04/29/qa-with-vlado-boza-2nd-place-winner-job-salary-prediction-competition/)

* **Neural Network是在这个比赛最成功的(前两名都用的是NN)。**

* [Q&A With Guocong Song, **3rd Prize**, Job Salary Prediction Competition](http://blog.kaggle.com/2013/04/23/qa-with-guocong-song-3rd-prize-job-salary-prediction-competition/)

* [Kaggle[3] - Job Salary Prediction (Adzuna) - 狂奔的番茄 - 博客频道 - CSDN.NET](http://blog.csdn.net/u011292007/article/details/37693521)

Github:

26/285 [https://github.com/likaiguo/kaggle-job-salary](https://github.com/likaiguo/kaggle-job-salary)

10/285 [git@github.com:Newmu/Salary-Prediction.git](git@github.com:Newmu/Salary-Prediction.git)

#### 2. 情商和可解释性
 * 考虑重新设置情商问题,特别是**[MBTI性格分析](http://note.youdao.com/share/?id=d9ee3b3e9622a93cf5860c3c3817d1d3&type=note)**
 * 主要的创新是:
 
 
 > **算薪资 = 基于大数据的薪资预测(理性) + 偏娱乐的性格测试(感性) + 比较八卦的星座测试 **
  
 

 
 
 
 
 
 
 
 
 
 
 
