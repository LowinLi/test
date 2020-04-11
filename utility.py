import pandas as pd
items = [
    '全部', '快乐', '乐观', '平静', '无助', '恐惧', '悲伤', '愤怒', '恐慌', '压力', '抑郁', '焦虑'
]
ps = [
    '广东', '北京', '山东', '江苏', '四川', '湖北', '上海', '河南', '河北', '福建', '安徽', '湖南',
    '重庆', '辽宁', '陕西', '广西', '黑龙江', '江西', '山西', '天津', '内蒙古', '云南', '吉林', '贵州',
    '新疆', '甘肃', '海南', '香港', '宁夏', '西藏', '台湾', '青海', '澳门'
]
py = [
    'guangdong', 'beijing', 'shandong', 'jiangsu', 'sichuan', 'hubei',
    'shanghai', 'henan', 'hebei', 'fujian', 'anhui', 'hunan', 'chongqing',
    'liaoning', 'shanxi', 'guangxi', 'heilongjiang', 'jiangxi', 'shanxi2',
    'tianjin', 'neimenggu', 'yunnan', 'jilin', 'guizhou', 'xinjiang', 'gansu',
    'hainan', 'xianggang', 'ningxia', 'xizang', 'taiwan', 'qinghai', 'aomen'
]
pro_df = pd.DataFrame({'c': ps, 'e': py})