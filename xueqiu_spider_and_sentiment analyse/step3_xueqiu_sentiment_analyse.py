from aip import AipNlp
import pandas as pd
import json
import time


# ======================baidu sentiment ai setup==========================

APP_ID = 'xxxxxx'
API_KEY = 'xxxxxxxxxxxxxxxxxxxx'
SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxx'

# 创建AipNlp实例,用于后续使用
aipNlp = AipNlp(APP_ID, API_KEY, SECRET_KEY)


# =======================func=============================

def posi_or_nega(comment, sleeping):
    time.sleep(sleeping)
    try:
        posi_prob = (aipNlp.sentimentClassify(comment))['items'][0]['positive_prob']
        # nega_prob = (aipNlp.sentimentClassify(comment))['items'][0]['negative_prob']
        if posi_prob > 0.7:
            return 1
        elif posi_prob < 0.3:
            return (-1)
        else:
            return 0
    except:
        return 'connection loss'


def check_loss(sentiment_col):
    loss_num = sentiment_col[sentiment_col == 'connection loss'].count()
    total_num = len(sentiment_col)
    loss_index = list(sentiment_col[sentiment_col == 'connection loss'].index)
    check_result = {
        'loss_number': loss_num,
        'loss_ratio': loss_num/total_num,
        'total_number': total_num,
        'loss_index': loss_index
    }
    return check_result

# ====================sentiment analyse=========================

comments_df = pd.read_csv('./cleaned_data/stock_comments_xueqiu.csv')

# middle point
# middle_point = 90001
# result = [0] * middle_point

result = []
comment = comments_df['title']
del comments_df

total = len(comment)

for i in range(total):
    print(f'正在判断第{i}行,共{total}行')
    a = posi_or_nega(comment[i], 0.5)
    result.append(a)
    if i % 5000 == 0:
        sa = pd.DataFrame(result)
        sa.to_csv(f'quicksave_{i}.csv')

sa = pd.DataFrame(result)
sa.to_csv(f'quicksave_final.csv')

# ===========================data_cleaning===========================

input = pd.read_csv('quick_save_final.csv',index_col=0)
comment = input[['title', 'sentiment']]
del input

check = comment['sentiment'] == 'connection loss'

total_loss = comment['sentiment'].loc[comment['sentiment'] == 'connection loss'].count()
total = len(comment)
loss = comment['sentiment'].tolist()
j = 0

for i in range(total):
    if check[i]:
        j += 1
        print(f'正在判断第{j}行,共{total_loss}行')
        while True:
            a = posi_or_nega(comment['title'][i], 0.5)
            if a == 1 or a == -1 or a == 0:
                break
            else:
                print('connection loss, retry...')
        loss[i] = a
        # if i % 5000 == 0:
        #     sa = pd.DataFrame(result)
        #     sa.to_csv(f'quicksave_{i}.csv')

# sa = pd.DataFrame(loss)
# sa.to_csv(f'final_loss.csv')

comment['final_sentiment'] = loss
comment.to_csv(f'final_loss.csv')