from typing import List

import pyecharts.options as opts
from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode
from pyecharts.charts import Timeline, Grid, Bar, Map, Pie, Line

import pandas as pd
from datetime import datetime, timedelta
from utility import items, pro_df
import pymongo
from render import *
db = pymongo.MongoClient('localhost', 27017).Emotion_Count_Db


def group_week(df):
    df['week'] = df['datetime'].apply(
        lambda x: x - timedelta(days=x.weekday()))
    datas = []
    for day, day_df in df.groupby('week'):
        data = [day]
        for item in items:
            data.append(day_df[item].sum())
        datas.append(data)
    new_df = pd.DataFrame(datas, columns=['week'] + items).iloc[1:-1]
    new_df.index = pd.to_datetime(new_df['week'])
    return new_df


def gen_data():
    total_num = []
    time_list = []
    datas = []
    df = pd.DataFrame(db['quanbu'].find())
    df = group_week(df)
    df['datetime'] = df.index
    for record in df.to_dict(orient='records'):
        dt = record['datetime']
        datas.append({'time': dt.strftime('%Y%m%d'), 'data': []})
        time_list.append(dt.strftime('%Y%m%d'))
        total_num.append(record['全部'])
    for record in pro_df.to_dict(orient='records'):
        print(record)
        df = pd.DataFrame(db[record['e']].find())
        df = group_week(df)
        i = 0
        for x in df.to_dict(orient='records'):
            pro_d = {'name': record['c'], 'value': [x['全部'], 0, record['c']]}
            datas[i]['data'].append(pro_d)
            i += 1
    maxN = 0
    for j in range(i):
        sorting_data = datas[j]['data']
        sorting_data = sorted(sorting_data, key=lambda x: x['value'][0],reverse=True)
        maxN = max(maxN, max([w['value'][0] for w in sorting_data]))
        datas[j]['data'] = sorting_data
    return datas, time_list, total_num, maxN

def gen_data_emotion(emot='压力'):
    print(emot)
    total_num = []
    time_list = []
    datas = []
    df = pd.DataFrame(db['quanbu'].find())
    df = group_week(df)
    df['datetime'] = df.index
    for record in df.to_dict(orient='records'):
        dt = record['datetime']
        datas.append({'time': dt.strftime('%Y%m%d'), 'data': []})
        time_list.append(dt.strftime('%Y%m%d'))
        total_num.append(record[emot]/record['全部']*10000)
    for record in pro_df.to_dict(orient='records'):
        df = pd.DataFrame(db[record['e']].find())
        df = group_week(df)
        i = 0
        for x in df.to_dict(orient='records'):
            if x[emot]<=5:
                continue
            pro_d = {'name': record['c'], 'value': [x[emot]/x['全部']*10000, 0, record['c']]}
            datas[i]['data'].append(pro_d)
            i += 1
    maxN = 0
    for j in range(i):
        sorting_data = datas[j]['data']
        sorting_data = sorted(sorting_data, key=lambda x: x['value'][0],reverse=True)
        maxN = max(maxN, max([w['value'][0] for w in sorting_data]))
        datas[j]['data'] = sorting_data
    return datas, time_list, total_num, maxN*5


def get_year_chart(year: str, title1, title2):
    map_data = [[[x["name"], x["value"]] for x in d["data"]] for d in data
                if d["time"] == year][0]
    min_data, max_data = (minNum, maxNum)
    data_mark: List = []
    i = 0
    for x in time_list:
        if x == year:
            data_mark.append(total_num[i])
        else:
            data_mark.append("")
        i = i + 1

    map_chart = (Map().add(
        series_name="",
        data_pair=map_data,
        zoom=1,
        center=[119.5, 34.5],
        is_map_symbol_show=False,
        itemstyle_opts={
            "normal": {
                "areaColor": "#323c48",
                "borderColor": "#404a59"
            },
            "emphasis": {
                "label": {
                    "show": Timeline
                },
                "areaColor": "rgba(255,255,255, 0.5)",
            },
        },
    ).set_global_opts(
        title_opts=opts.TitleOpts(
            title="" + str(year) + title1,
            subtitle="",
            pos_left="center",
            pos_top="top",
            title_textstyle_opts=opts.TextStyleOpts(
                font_size=25, color="rgba(255,255,255, 0.9)"),
        ),
        tooltip_opts=opts.TooltipOpts(
            is_show=True,
            formatter=JsCode("""function(params) {
                    if ('value' in params.data) {
                        return params.data.value[2] + ': ' + params.data.value[0];
                    }
                }"""),
        ),
        visualmap_opts=opts.VisualMapOpts(
            is_calculable=True,
            dimension=0,
            pos_left="30",
            pos_top="center",
            range_text=["High", "Low"],
            range_color=["lightskyblue", "yellow", "orangered"],
            textstyle_opts=opts.TextStyleOpts(color="#ddd"),
            min_=min_data,
            max_=max_data,
        ),
    ))

    line_chart = (Line().add_xaxis(time_list).add_yaxis(
        "", total_num).add_yaxis(
            "",
            data_mark,
            markpoint_opts=opts.MarkPointOpts(
                data=[opts.MarkPointItem(type_="max")]),
        ).set_series_opts(label_opts=opts.LabelOpts(
            is_show=False)).set_global_opts(title_opts=opts.TitleOpts(
                title=title2, pos_left="72%", pos_top="5%")))
    bar_x_data = [x[0] for x in map_data]
    bar_y_data = [{"name": x[0], "value": x[1][0]} for x in map_data]
    bar = (Bar().add_xaxis(xaxis_data=bar_x_data).add_yaxis(
        series_name="",
        yaxis_data=bar_y_data,
        label_opts=opts.LabelOpts(is_show=True,
                                  position="right",
                                  formatter="{b} : {c}"),
    ).reversal_axis().set_global_opts(
        xaxis_opts=opts.AxisOpts(max_=maxNum,
                                 axislabel_opts=opts.LabelOpts(is_show=False)),
        yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(is_show=False)),
        tooltip_opts=opts.TooltipOpts(is_show=False),
        visualmap_opts=opts.VisualMapOpts(
            is_calculable=True,
            dimension=0,
            pos_left="10",
            pos_top="top",
            range_text=["High", "Low"],
            range_color=["lightskyblue", "yellow", "orangered"],
            textstyle_opts=opts.TextStyleOpts(color="#ddd"),
            min_=min_data,
            max_=max_data,
        ),
    ))

    pie_data = [[x[0], x[1][0]] for x in map_data]
    pie = (Pie().add(
        series_name="",
        data_pair=pie_data,
        radius=["15%", "35%"],
        center=["80%", "82%"],
        itemstyle_opts=opts.ItemStyleOpts(border_width=1,
                                          border_color="rgba(0,0,0,0.3)"),
    ).set_global_opts(
        tooltip_opts=opts.TooltipOpts(is_show=True, formatter="{b} {d}%"),
        legend_opts=opts.LegendOpts(is_show=False),
    ))

    grid_chart = (Grid().add(
        bar,
        grid_opts=opts.GridOpts(pos_left="10",
                                pos_right="45%",
                                pos_top="50%",
                                pos_bottom="5"),
    ).add(
        line_chart,
        grid_opts=opts.GridOpts(pos_left="65%",
                                pos_right="80",
                                pos_top="10%",
                                pos_bottom="50%"),
    ).add(pie, grid_opts=opts.GridOpts(pos_left="45%", pos_top="60%")).add(
        map_chart, grid_opts=opts.GridOpts()))

    return grid_chart

def render(input_d):
    data, time_list, total_num, maxNum, output_name,title1, title2 = input_d
    minNum = 1
    timeline = Timeline(init_opts=opts.InitOpts(
        width="1520px", height="720px", theme=ThemeType.DARK))
    for y in time_list:
        g = get_year_chart(y, title1,title2)
        timeline.add(g, time_point=str(y))

    timeline.add_schema(
        orient="vertical",
        is_auto_play=True,
        is_inverse=True,
        play_interval=5000,
        pos_left="null",
        pos_right="5",
        pos_top="20",
        pos_bottom="20",
        width="73",
        label_opts=opts.LabelOpts(is_show=True, color="#fff"),
    )
    timeline.render(output_name)
if __name__ == "__main__":
    data, time_list, total_num, maxNum = gen_data()
    render(tuple([data, time_list, total_num, maxNum, "html/人民日报评论数.html", "全国各省在人民日报微博上的评论数 数据来源：微博","全国微博评论数每周变化" ]))
    from utility import items
    for emot in items[1:]:
        data, time_list, total_num, maxNum =gen_data_emotion(emot)
        render(tuple([data, time_list, total_num, maxNum, "html/%s.html"%emot, "全国各省在人民日报微博上的情感占比：%s 数据来源：微博"%emot,"全国微博情感每周变化："+emot]))