###API

####生成分享图片
#####接口
GET  /share_picture?data=
##### 请求参数
| 名称 | 类型 |定义  |说明

| url    |string |需要生成图片的网页地址 |

| height | int | 高度 |中心点向上下扩展

|width | int |宽度 |中心点向两边扩展

|box | array | 坐标|(left,upper,right,lower)

|name | string | 前缀名称 |


##### 响应

###### 成功: 200
###### 响应格式 : json
{
    img_url: "" ,//生成图片地址
    status: "ok"
    
}
  
###### 失败:200
###### 响应格式:json
{
    status:"error",
    msg:"" //错误消息
}



#####接口
GET  /predict_feedback?id=
##### 请求参数
| 名称 | 类型 |定义  |说明

| id    |string |请求的计算id |

| accuracy|int |高 准 低 == 1 0 -1 |

#####接口
GET  /share_plantform?id=
##### 请求参数
| 名称 | 类型 |定义  |说明

| id    |string |请求的计算id |

| plantform|int | 微博 QQ空间 微信 (wb qz wx) |
