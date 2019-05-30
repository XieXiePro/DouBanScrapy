#-*- coding: utf-8 -*-
import pymysql
import pandas as pd
from sklearn.cluster import KMeans
from pandas import DataFrame
from scipy.cluster.hierarchy import linkage,dendrogram
import matplotlib.pyplot as plt

if __name__ == '__main__':
    conn = pymysql.connect(host="localhost",
                           user="root",
                           password="xieping",
                           database="estore",)

    cursor = conn.cursor()
    sql = "select * from DB"
    cursor.execute(sql)
    results = cursor.fetchall()

    resultList = []

    for result in results:
        resultList.append(result)

    # print(resultList)

    df = DataFrame(resultList)
    # print(df.head())

    # 绘制散点图 评分，参与评论人数
    plt.figure(figsize=(10, 8))
    plt.scatter(df[8].astype(float), df[7].astype(float))
    plt.show()

    scoreDf = pd.DataFrame(df, columns=[7])
    scoreDf.head()

    k = 6  # 聚类的类别
    iteration = 500  # 聚类最大循环次数
    model = KMeans(n_clusters=k,
                   n_jobs=1,
                   max_iter=iteration)  # 分为k类，并发数1，数值大系统卡死
    model.fit(scoreDf)  # 开始聚类

    # 详细输出原始数据及其类别
    res = pd.concat([df,
                     pd.Series(model.labels_, index=df.index)],
                    axis=1)  # 详细输出每个样本对应的类别
    res.columns = list(df.columns) + [u'class']  # 重命名表头

    # 根据聚类画出分类统计图
    for col in res.columns:
        if col in [u'class']:
            fig = plt.figure()
            res[col].hist(bins=20)
            fig.show()

    res.to_excel('knn_result.xls')  # 保存结果