### 运行配置错误
问题1，错误信息
```
Exception in thread "main" java.lang.Exception: When running with master 'yarn' either HADOOP_CONF_DIR or YARN_CONF_DIR must be set in the environment.
```
解决方案
```
export HADOOP_CONF_DIR=/etc/hadoop/conf
```
问题2，错误信息
```
org.apache.hadoop.security.AccessControlException: Permission denied: user=bigdata, access=WRITE, inode="/user/bigdata":hdfs:supergroup:drwxr-xr-x
```
解决方案
```
export HADOOP_USER_NAME=hdfs
```
问题3，错误信息
```
ImportError: cannot import name 'PandasUDFType'
```
解决方案
```
关闭虚拟环境，然后重新启动虚拟环境
$ deactive
$ workon bi-analysis
```
问题4，错误信息
```
ModuleNotFoundError: No module named 'bi'
```
解决方案
```
export PYTHONPATH=$(pwd)
```


### Spark的运行模式
Spark也可以运行在多种模式之上，主要有以下4种运行模式:

  1. local: 本地单进程模式，用于本地开发测试spark代码
  2. standalone: 分布式集群模式，Master-Worker架构，Master负责调度，Worker负责具体Task的执行
  3. on yarn/mesos: 运行在yarn/mesos等资源管理架构之上，yarn/mesos提供资源管理，spark提供计算调度，并可与其他计算框架（如MapReduce/MPI/Storm）共同运行在同一个集群之上
  4. on cloud(EC2): 运行在AWS的EC2之上

### spark的安装（本地模式）