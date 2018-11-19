# bi-analysis(BI系统统计分析)

### 安装环境
- [spark下载安装](http://spark.apache.org/downloads.html)
- mkvirtualenv -p python3 bi-analysis
- pip install -r requirements.txt
    - 通过此命令安装失败的包，可直接通过 pip install 包名 进行安装


### 项目结构
- bi
    - core          项目核心方法
    - preprocess    预处理
        - preprocess_main.py    预处理主函数
        - resume_profile.py     简历基本信息预处理
        - resume_educations.py  简历教育经历预处理
        - resume_works.py       简历工作经历预处理
        - job_profile.py        职位数据预处理
    - settings      项目设置
    - statistic     统计分析
        - main.py     统计分析主函数
        - school.py   学校维度的统计
        - major.py    专业维度的统计
        - company.py     公司维度的统计
        - industry.py   行业维度的统计
        - industry_address.py             行业+地域维度的统计
        - industry_position_address.py    行业+职位+地域维度的统计
        - position.py             职位维度的统计
        - position_address.py     职位+地域维度的统计
        - school_major.py     学校+专业维度的统计
        - postgraduate.py     学校+专业维度的深造情况统计
        - job.py     招聘职位情况统计
        - person.py     个人情况统计
        - search.py     搜索相关统计
    - utils         工具函数