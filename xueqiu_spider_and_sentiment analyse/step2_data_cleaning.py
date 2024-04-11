import pandas as pd
import os
import datetime
import re


def get_file_creation_date(file_path):
    """
    获取文件的创建日期
    """
    # 获取文件的创建时间戳
    creation_timestamp = os.path.getctime(file_path)

    creation_datetime = datetime.datetime.fromtimestamp(creation_timestamp)

    formatted_date = creation_datetime.strftime('%m-%d')

    return formatted_date


def get_all_csv(folder_path):
    return [file for file in os.listdir(folder_path) if file.endswith('.csv')]


def main():

    result = pd.DataFrame()

    all_csv = get_all_csv('./result')

    start_date = pd.to_datetime('2024-03-01')

    for this_csv in all_csv:

        print(f'cleaning{this_csv}')

        file_path = f'./result/{this_csv}'

        create_time = get_file_creation_date(file_path)

        raw = pd.read_csv(file_path)

        clip = raw[['id', 'timeBefore', 'description', 'view_count', 'user', 'reply_count', 'source']]

        # change “**分钟前” comments to actual date
        clip.loc[clip['timeBefore'].str.contains('前'), 'timeBefore'] = create_time + " 00:00"
        # change “今天 **” comments to actual date
        clip.loc[clip['timeBefore'].str.contains('今天'), 'timeBefore'] = create_time + " 00:00"

        # not automatically match, simplified for the project.
        clip.loc[~clip['timeBefore'].str.contains('202'), 'timeBefore'] = '2024-' + clip['timeBefore']

        clip.loc[:, 'timeBefore'] = pd.to_datetime(clip['timeBefore'])

        clip = clip[clip['timeBefore'] >= start_date].copy()

        output = clip.copy()

        output.loc[:, 'stock'] = this_csv[2:8]

        # time_clip['stock'] = time_clip['stock'].astype(str)

        # get the author name
        output.loc[:, 'user'] = output['user'].apply(lambda x: eval(x)['screen_name'])

        # get the source
        output.loc[~output['source'].str.contains('雪球'), 'source'] = '雪球' + output['source']

        # the key: id,  add the resource?
        # time_clip['id'] = 'xq' + time_clip['id'].astype(str)

        output['description'] = output['description'].astype(str)
        output.loc[:, 'description'] = output['description'].apply(lambda x: re.sub(r'<[^>]+>', '', x))

        # reindex the columns
        output = output.reindex(
            columns=['id', 'stock', 'view_count', 'reply_count', 'description', 'user', 'timeBefore', 'source'])

        output.columns = ['post_id', 'stock_index', 'read_counts', 'comment_counts', 'title', 'author',
                             'update_time',
                             'source']

        result = pd.concat([result, output], axis=0)

        # output.to_csv(f'./cleaned_data/{this_csv}', encoding='utf-8', index=False)
    result = result.dropna()
    result.to_csv(f'./cleaned_data/stock_comments_xueqiu.csv', encoding='utf-8', index=False)

main()