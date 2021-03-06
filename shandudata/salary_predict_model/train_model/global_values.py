# coding:utf-8
'''
Created on 2014年12月23日

@author: likaiguo
'''
feature_columns_dict = \
{
    "age": {
    "0": 0,
    "10": 10,
    "13": 13,
    "14": 14,
    "15": 15,
    "16": 16,
    "17": 17,
    "18": 18,
    "19": 19,
    "20": 20,
    "2013": 2013,
    "21": 21,
    "22": 22,
    "23": 23,
    "24": 24,
    "25": 25,
    "26": 26,
    "27": 27,
    "28": 28,
    "29": 29,
    "30": 30,
    "31": 31,
    "32": 32,
    "33": 33,
    "34": 34,
    "35": 35,
    "36": 36,
    "37": 37,
    "38": 38,
    "39": 39,
    "40": 40,
    "41": 41,
    "42": 42,
    "43": 43,
    "44": 44,
    "45": 45,
    "46": 46,
    "47": 47,
    "48": 48,
    "49": 49,
    "50": 50,
    "51": 51,
    "52": 52,
    "53": 53,
    "54": 54,
    "55": 55,
    "56": 56,
    "57": 57,
    "58": 58,
    "59": 59,
    "60": 60,
    "61": 61,
    "62": 62,
    "65": 65,
    "70": 70
  },
    "city": {
        "七台河": 299,
    "三亚": 14,
    "三河": 123,
    "三门峡": 41,
    "上海": 247,
    "上饶": 46,
    "东方": 365,
    "东莞": 43,
    "东营": 401,
    "东阳": 20,
    "中卫": 262,
    "中山": 115,
    "临汾": 101,
    "临沂": 57,
    "临沧": 65,
    "丹东": 277,
    "丹阳": 270,
    "丽水": 326,
    "义乌": 99,
    "乌兰察布": 364,
    "乌海": 127,
    "乌鲁木齐": 94,
    "乐山": 125,
    "乐清": 50,
    "九江": 342,
    "乳山": 424,
    "云南": 8,
    "云南省": 336,
    "云浮": 316,
    "五指山": 82,
    "亳州": 224,
    "仙桃": 108,
    "伊春": 40,
    "伊犁哈萨克自治州": 9,
    "余姚": 56,
    "佛山": 7,
    "佳木斯": 369,
    "保定": 144,
    "保山": 114,
    "信阳": 172,
    "克拉玛依": 411,
    "全国": 242,
    "公主岭": 226,
    "六安": 280,
    "六盘水": 218,
    "兰州": 68,
    "兴安盟": 394,
    "内江": 55,
    "内蒙古": 246,
    "凉山": 24,
    "凉山彝族自治州": 290,
    "包头": 104,
    "北京": 319,
    "北海": 307,
    "十堰": 134,
    "南京": 425,
    "南充": 0,
    "南宁": 37,
    "南平": 379,
    "南昌": 386,
    "南通": 73,
    "南阳": 237,
    "厦门": 33,
    "双城": 409,
    "双鸭山": 176,
    "台州": 109,
    "台湾": 88,
    "台湾省": 181,
    "合肥": 139,
    "吉安": 170,
    "吉林": 388,
    "吉林市": 361,
    "吉林省": 422,
    "吐鲁番": 66,
    "吕梁": 81,
    "吴忠": 220,
    "吴江": 416,
    "周口": 44,
    "呼伦贝尔": 257,
    "呼和浩特": 138,
    "和田": 186,
    "和顺": 358,
    "咸宁": 191,
    "咸阳": 314,
    "哈密": 408,
    "哈尔滨": 256,
    "唐山": 382,
    "商丘": 214,
    "商洛": 199,
    "嘉兴": 410,
    "嘉峪关": 285,
    "四川": 110,
    "四川省": 318,
    "四平": 86,
    "固安": 203,
    "国外": 36,
    "大兴安岭": 213,
    "大同": 351,
    "大庆": 61,
    "大理白族自治州": 169,
    "大连": 276,
    "天水": 312,
    "天津": 376,
    "天门": 419,
    "太仓": 320,
    "太仓市": 95,
    "太原": 173,
    "威海": 91,
    "娄底": 187,
    "孝感": 141,
    "宁夏": 70,
    "宁德": 428,
    "宁波": 232,
    "宁海": 265,
    "安庆": 266,
    "安康": 47,
    "安徽": 102,
    "安徽省": 385,
    "安阳": 22,
    "安顺": 317,
    "定西": 63,
    "宜兴": 129,
    "宜城": 207,
    "宜宾": 21,
    "宜昌": 298,
    "宜春": 309,
    "宝鸡": 412,
    "宣城": 393,
    "宿州": 34,
    "宿迁": 26,
    "山东": 215,
    "山东省": 283,
    "山西": 78,
    "山西省": 16,
    "岳阳": 275,
    "峨眉": 322,
    "崇左": 195,
    "巢湖": 400,
    "巴中": 366,
    "巴彦淖尔": 404,
    "巴音郭楞": 413,
    "巴音郭楞蒙古自治州": 370,
    "常州": 80,
    "常德": 156,
    "常熟": 264,
    "平凉": 305,
    "平顶山": 106,
    "广东": 345,
    "广东省": 59,
    "广元": 105,
    "广安": 164,
    "广州": 272,
    "广德": 371,
    "广西": 93,
    "庆阳": 113,
    "廊坊": 228,
    "延安": 147,
    "延边": 357,
    "延边朝鲜族自治州": 334,
    "开封": 54,
    "开平": 234,
    "张家口": 302,
    "张家港": 11,
    "张家界": 168,
    "张掖": 367,
    "徐州": 397,
    "德州": 350,
    "德阳": 269,
    "忻州": 363,
    "怀化": 154,
    "恩施": 85,
    "恩施土家族苗族自治州": 387,
    "惠州": 405,
    "慈溪": 399,
    "成都": 142,
    "扬州": 84,
    "承德": 151,
    "抚州": 343,
    "抚顺": 160,
    "拉萨": 321,
    "揭阳": 39,
    "攀枝花": 87,
    "文山壮族苗族自治州": 136,
    "新乡": 178,
    "新余": 119,
    "新疆": 31,
    "新疆维吾尔自治区": 289,
    "无锡": 222,
    "日照": 152,
    "昆山": 359,
    "昆明": 230,
    "昌吉回族自治州": 241,
    "昌江黎族自治县": 389,
    "昌都": 420,
    "昭通": 333,
    "晋中": 153,
    "晋城": 148,
    "普宁": 117,
    "景德镇": 77,
    "曲靖": 253,
    "朔州": 301,
    "朝阳": 60,
    "本溪": 209,
    "来宾": 331,
    "杨凌": 310,
    "杭州": 100,
    "松原": 76,
    "枣庄": 348,
    "柳州": 42,
    "株洲": 355,
    "桂林": 98,
    "桐乡": 128,
    "梅州": 282,
    "梧州": 250,
    "楚雄彝族自治州": 162,
    "榆林": 28,
    "武威": 349,
    "武汉": 51,
    "毕节": 353,
    "永州": 179,
    "汉中": 324,
    "汕头": 182,
    "汕尾": 340,
    "江苏": 225,
    "江苏省": 64,
    "江西": 377,
    "江西省": 360,
    "江门": 197,
    "江阴": 23,
    "池州": 52,
    "沈阳": 286,
    "沧州": 423,
    "河北": 17,
    "河北省": 396,
    "河南": 3,
    "河南省": 38,
    "河池": 380,
    "河源": 294,
    "泉州": 293,
    "泉港区": 233,
    "泰兴": 190,
    "泰安": 72,
    "泰州": 372,
    "泸州": 263,
    "洛阳": 188,
    "济南": 161,
    "济宁": 204,
    "济源": 368,
    "浙江": 344,
    "浙江省": 415,
    "海东": 288,
    "海南": 284,
    "海南省": 217,
    "海口": 15,
    "海西": 143,
    "淄博": 374,
    "淮北": 74,
    "淮南": 58,
    "淮安": 126,
    "深圳": 231,
    "清远": 4,
    "温岭": 185,
    "温州": 146,
    "渭南": 258,
    "湖北": 229,
    "湖北省": 205,
    "湖南": 244,
    "湖南省": 137,
    "湖州": 121,
    "湘潭": 122,
    "湘西土家族苗族自治州": 62,
    "湛江": 255,
    "溧阳": 107,
    "滁州": 300,
    "滨州": 395,
    "漯河": 124,
    "漳州": 2,
    "潍坊": 248,
    "潜江": 166,
    "潮州": 155,
    "澄迈": 116,
    "澳门": 89,
    "濮阳": 338,
    "烟台": 158,
    "焦作": 133,
    "燕郊开发区": 332,
    "牡丹江": 120,
    "玉林": 96,
    "玉溪": 49,
    "玉环县": 271,
    "珠海": 356,
    "琼中黎族苗族自治县": 278,
    "琼海": 240,
    "甘孜藏族自治州": 183,
    "白城": 251,
    "白山": 383,
    "白银": 417,
    "百色": 406,
    "益阳": 306,
    "盐城": 414,
    "盘锦": 192,
    "眉山": 308,
    "石嘴山": 135,
    "石家庄": 167,
    "石河子": 10,
    "福安": 274,
    "福州": 159,
    "福建": 5,
    "福建省": 150,
    "秦皇岛": 418,
    "简阳": 235,
    "红河哈尼族彝族自治州": 243,
    "红河州": 75,
    "绍兴": 216,
    "绥化": 219,
    "绵阳": 287,
    "聊城": 184,
    "肇庆": 171,
    "胶南": 69,
    "自贡": 315,
    "舟山": 426,
    "芜湖": 339,
    "苏州": 177,
    "茂名": 29,
    "荆州": 83,
    "荆门": 92,
    "荣成": 145,
    "莆田": 6,
    "莱芜": 296,
    "菏泽": 268,
    "萍乡": 279,
    "营口": 295,
    "葫芦岛": 193,
    "蚌埠": 384,
    "衡水": 201,
    "衡阳": 211,
    "衢州": 180,
    "襄阳": 53,
    "西双版纳傣族自治州": 375,
    "西宁": 325,
    "西安": 323,
    "西昌": 196,
    "西藏自治区": 97,
    "许昌": 157,
    "诸暨": 163,
    "贵州": 25,
    "贵州省": 354,
    "贵港": 79,
    "贵阳": 32,
    "贺州": 249,
    "资阳": 252,
    "赣州": 90,
    "赤峰": 421,
    "辽宁": 337,
    "辽宁省": 202,
    "辽源": 174,
    "辽阳": 200,
    "达州": 335,
    "运城": 238,
    "连云港": 330,
    "通化": 245,
    "通州": 111,
    "通辽": 132,
    "遂宁": 292,
    "遵义": 71,
    "邢台": 227,
    "那曲": 297,
    "邯郸": 236,
    "邵阳": 149,
    "郑州": 427,
    "郴州": 206,
    "鄂尔多斯": 378,
    "鄂州": 391,
    "酒泉": 198,
    "重庆": 130,
    "金华": 221,
    "金昌": 67,
    "钦州": 194,
    "铁岭": 347,
    "铜川": 329,
    "铜陵": 303,
    "银川": 352,
    "锡林郭勒盟": 390,
    "锦州": 210,
    "镇江": 165,
    "长春": 407,
    "长沙": 261,
    "长治": 254,
    "长葛": 304,
    "阜新": 362,
    "阜阳": 273,
    "防城港": 189,
    "阳江": 341,
    "阳泉": 313,
    "阿克苏": 398,
    "阿坝": 35,
    "阿坝藏族羌族自治州": 311,
    "阿拉尔": 30,
    "陇南": 267,
    "陕西": 291,
    "陕西省": 327,
    "随州": 212,
    "雅安": 223,
    "青岛": 103,
    "青海": 1,
    "靖江": 45,
    "鞍山": 259,
    "韶关": 373,
    "顺德": 392,
    "香河": 12,
    "香港": 131,
    "香港特别行政区": 48,
    "马鞍山": 403,
    "驻马店": 328,
    "鸡西": 19,
    "鹤岗": 18,
    "鹰潭": 13,
    "黄冈": 140,
    "黄山": 381,
    "黄石": 239,
    "黑河": 27,
    "黑龙江": 260,
    "黑龙江省": 346,
    "黔东南": 402,
    "黔东南苗族侗族自治州": 118,
    "黔南": 208,
    "黔西南布依族苗族自治州": 281,
    "齐齐哈尔": 175,
    "龙岩": 112
  },
    "degree": {
        "": 0,

    "中专": 1,
    "中技": 1,
    "其他": 2,
    "初中": 1,
    "高中": 1,

    "大专": 3,
    '专科': 3,
    "本科": 5,
    "硕士": 7,
    "研究生": 7,

    "EMBA": 7,
    "MBA": 7,
    'MBA/EMBA': 7,

    "博士": 10,
    "博士后": 10,
    # 大专 本科 硕士 其他 中专 中技 高中 博士 EMBA MBA MBA/EMBA 博士后 初中
  },
    "first_class": {
        "": 0,
    "产品": 5,
    "市场与销售": 1,
    "技术": 4,
    "游戏": 3,
    "电商": 2,
    "职能": 8,
    "设计": 7,
    "运营": 6
  },
    "gender": {
        "女": 0,
    "男": 1
  },
    "lower_salary": {
        "1000": 1000,
    "10001": 10001,
    "12500": 12500,
    "15000": 15000,
    "1666": 1666,
    "2001": 2001,
    "2500": 2500,
    "25000": 25000,
    "3333": 3333,
    "4001": 4001,
    "4166": 4166,
    "41666": 41666,
    "500": 500,
    "5000": 5000,
    "6001": 6001,
    "6666": 6666,
    "8001": 8001,
    "833": 833,
    "8333": 8333,
    "83333": 83333
  },
    "school_level": {
        "": 0,
    "中国一流大学": 10,
    "中国知名大学": 4,
    "中国顶尖大学": 6,
    "中国高水平大学": 14,
    "中学以下": 9,
    "党政军大学": 15,
    "国外大学": 11,
    "学院职业技术": 12,
    "学院职业技术中学以下": 3,
    "普通二本学院": 8,
    "普通大学": 2,
    "职业技术": 1,
    "进修": 7,
    "进修学院职业技术": 5,
    "进修职业技术": 13
  },
    "upper_salary": {
        "1000": 1000,
    "10000": 10000,
    "12500": 12500,
    "15000": 15000,
    "1666": 1666,
    "166666": 166666,
    "2000": 2000,
    "2500": 2500,
    "25000": 25000,
    "3333": 3333,
    "4000": 4000,
    "4166": 4166,
    "41666": 41666,
    "5000": 5000,
    "50000": 50000,
    "6000": 6000,
    "6666": 6666,
    "8000": 8000,
    "8333": 8333,
    "83333": 83333
  },
    "work_len": {
        "0": 0,
    "1": 1,
    "10": 10,
    "1003": 1003,
    "1004": 1004,
    "11": 11,
    "12": 12,
    "13": 13,
    "14": 14,
    "15": 15,
    "16": 16,
    "17": 17,
    "18": 18,
    "19": 19,
    "2": 2,
    "20": 20,
    "21": 21,
    "22": 22,
    "23": 23,
    "24": 24,
    "25": 25,
    "26": 26,
    "3": 3,
    "33": 33,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9
  }
}
feature_columns_dict = {k: {x.decode('utf-8'): y for x, y in v.items()}for k, v in feature_columns_dict.items()}
