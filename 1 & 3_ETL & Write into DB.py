# -*- coding: utf-8 -*-
from lib import Regex
from lib import SQLAlchemy
import pandas as pd
import numpy as np


# ---------------------------------------------------------------------------------------------------- #
# Import Data and Function
# ---------------------------------------------------------------------------------------------------- #
# Function - Regular Expression
regex = Regex()

# Function - Database
sqlalchemy = SQLAlchemy(Database_Type='mysql',
                        User='###your username###',
                        Pwd='###your password###',
                        Host='###your host###',
                        Port='###your port###',
                        Database='###your database name###')

# df_tt_sku_sample
df_tt_sku = pd.read_csv('./df_tt_sku_sample.csv')
quantity_Sum = df_tt_sku['quantity'].sum()

# mpn_sample
dict_df_mpn_sub = {}    # Place the sub-collection of df_mpn
df_mpn = pd.read_csv('./mpn_sample.csv', encoding='ANSI')

df_mpn.rename(columns={'code': 'id'}, inplace=True)
df_mpn['idx'] = df_mpn['id']
df_mpn = df_mpn.set_index('idx')

count_rows = 0
count_cols = df_mpn.shape[1]
for i in df_mpn['category'].unique():
    df_mpn_sub = df_mpn[df_mpn['category'] == i]

    count_rows += df_mpn_sub.shape[0]
    assert count_cols == df_mpn_sub.shape[1], '[WARNING] Number of columns is different between parent and sub-collection.'
    dict_df_mpn_sub.update({i: df_mpn_sub})

assert count_rows == df_mpn.shape[0], '[WARNING] Number of rows is different between parent and sub-collection.'

# Value for filling empty
empty_value = r' '


# ---------------------------------------------------------------------------------------------------- #
# sku_noplus
#
# ---------------------------------------------------------------------------------------------------- #
df_tt_sku['sku_noplus'] = df_tt_sku['sku']


# ---------------------------------------------------------------------------------------------------- #
# 將欄位 sku 用 '-' 切割成兩個欄位 sku1 及 sku2
# sku1, sku2 欄位開頭不可有空格
# ---------------------------------------------------------------------------------------------------- #
df_tt_sku[['sku1', 'sku2']] = df_tt_sku.sku.str.split('-', expand=True)
df_tt_sku['sku1'] = df_tt_sku['sku1'].str.lstrip(' ')
df_tt_sku['sku2'] = df_tt_sku['sku2'].str.lstrip(' ')


# ---------------------------------------------------------------------------------------------------- #
# 新增 nchar 欄位
# nchar 為 sku1 的字元長度
# ---------------------------------------------------------------------------------------------------- #
df_tt_sku['nchar'] = df_tt_sku['sku1'].str.len()


# ---------------------------------------------------------------------------------------------------- #
# 新增 sku_num & ndigit 欄位
# 先將 3PB 取代成空，因為字頭 '3PB' 的 '3' 不記入數字部分
#
# ---------------------------------------------------------------------------------------------------- #
df_tt_sku['sku_num'] = df_tt_sku['sku1'].str.replace('3PB', '')
df_tt_sku['sku_num'] = df_tt_sku['sku_num'].apply(
    lambda x: regex.extract_numbers(x))
df_tt_sku['ndigit'] = df_tt_sku['sku_num'].str.len()


# ---------------------------------------------------------------------------------------------------- #
# 新增 sku_head 欄位
# 用正規表達式來取 sku1 英文部分作為 sku_head (sku_head 取字串開頭)
# 若包含 '3PB' 則 sku_head 替換為 '3PB'
# 若包含 'MA' 或 'NX' 則 sku_head 替換為 'MA' 或 'NX'
# ---------------------------------------------------------------------------------------------------- #
df_tt_sku['sku_head'] = df_tt_sku['sku1'].apply(
    lambda x: regex.extract_head_with_nums_and_chars(x))

df_tt_sku['sku_head'] = df_tt_sku['sku_head'].replace(
    r'\w*3PB\w*', '3PB', regex=True)

df_tt_sku['sku_head'] = df_tt_sku['sku_head'].replace(
    r'\w*MA\w*', 'MA', regex=True)

df_tt_sku['sku_head'] = df_tt_sku['sku_head'].replace(
    r'\w*NX\w*', 'NX', regex=True)


# ---------------------------------------------------------------------------------------------------- #
# 新增 sku_tail_id 欄位
# 抓 sku1 的最後一個英文字元，若不是英文則不要
# ---------------------------------------------------------------------------------------------------- #
# df_tt_sku['sku_tail_id'] = np.where(
#     (df_tt_sku['sku1'].str.strip().str[-1]).str.isalpha(),
#     (df_tt_sku['sku1'].str.strip().str[-1]),
#     np.nan)

df_tt_sku['sku_tail_id'] = np.where(
    (df_tt_sku['sku1'].str.strip().str[-1]).str.match(pat='[a-zA-Z]'),
    (df_tt_sku['sku1'].str.strip().str[-1]),
    np.nan)


# ---------------------------------------------------------------------------------------------------- #
# 新增 brand_id 欄位
# 若 nchar 大於 5 則取 sku_num 的前兩碼當成 brand_id
# ---------------------------------------------------------------------------------------------------- #
df_tt_sku.loc[
    df_tt_sku['nchar'] > 5, 'brand_id'] = df_tt_sku['sku_num'].str[:2]


# ---------------------------------------------------------------------------------------------------- #
# 新增 model_id 欄位
# 取 sku_num 的 第3到5個數字為 model_id
# ---------------------------------------------------------------------------------------------------- #
df_tt_sku['model_id'] = df_tt_sku['sku_num'].str[2:5]
# df_tt_sku['model_id'] = df_tt_sku['sku_num'].apply(
#     lambda x: x[2:5] if len(x[2:5]) > 0 else np.nan)


# ---------------------------------------------------------------------------------------------------- #
# 新增 design_id 欄位
# 留下 sku2 的英文字母部分
# 撰寫函式使用正規表達式，並使用 lambda 回傳資料
# ---------------------------------------------------------------------------------------------------- #
df_tt_sku['design_id'] = df_tt_sku['sku2'].apply(
    lambda x: regex.extract_characters(x, return_type='str'))


# ---------------------------------------------------------------------------------------------------- #
# 以 tt_sku_sample 為主，將 mpn_sample 對應至 tt_sku_sample (join or merge)
# Join 前先篩選 mpn_sample category 等於  sku_head、brand、model、tail 的 row data
# 用 tt_sku_sample 對應欄位:  sku_head、brand、model、tail  來  join mpn_sample 的 code 欄位
# ---------------------------------------------------------------------------------------------------- #
df_sku_head = dict_df_mpn_sub.get('sku_head')
df_sku_head = df_sku_head[['id', 'Type', 'name']]
df_sku_head.rename(columns={'name': 'product'}, inplace=True)
df_tt_sku = df_tt_sku.join(
    df_sku_head[['Type', 'product']], on='sku_head', how='left')

df_brand = dict_df_mpn_sub.get('brand')
df_brand = df_brand[['id', 'name']]
df_brand.rename(columns={'name': 'brand'}, inplace=True)
df_tt_sku = df_tt_sku.join(
    df_brand['brand'], on='brand_id', how='left')

df_model = dict_df_mpn_sub.get('model')
df_model = df_model[['id', 'name']]
df_model.rename(columns={'name': 'model'}, inplace=True)
df_tt_sku = pd.merge(df_tt_sku, df_model['model'], left_on='model_id',
                     right_index=True, how='left')

df_sku_tail = dict_df_mpn_sub.get('sku_tail')
df_sku_tail = df_sku_tail[['id', 'name']]
df_sku_tail.rename(columns={'name': 'sku_tail'}, inplace=True)
df_tt_sku = pd.merge(df_tt_sku, df_sku_tail['sku_tail'], left_on='sku_tail_id',
                     right_index=True, how='left')


# ---------------------------------------------------------------------------------------------------- #
# 利用 ‘sku_tail_id’ 欄位，進行邏輯判斷，來填入 Type 欄位符合邏輯的值
# 將 sku_tail_id 轉換為大寫字母
# 若 sku_tail_id 欄位值為 K ，則填入 'Bu'
# 若 sku_tail_id 欄位值為 E ，則填入 'Rim'
# ---------------------------------------------------------------------------------------------------- #
df_tt_sku['sku_tail_id'] = df_tt_sku['sku_tail_id'].str.upper()

df_tt_sku.loc[df_tt_sku['sku_tail_id'] == 'K', 'Type'] = 'Bu'
df_tt_sku.loc[df_tt_sku['sku_tail_id'] == 'E', 'Type'] = 'Rim'


# ---------------------------------------------------------------------------------------------------- #
# 將 nan 取代為 r' '
# 把所有欄位為nan的資料取代為 r' '
# ---------------------------------------------------------------------------------------------------- #
df_tt_sku = df_tt_sku.fillna(value=empty_value)


# ---------------------------------------------------------------------------------------------------- #
# 資料存入 MySQL
# ---------------------------------------------------------------------------------------------------- #
sqlengine = sqlalchemy.create_engine()

# Solution for solving the Error 1452(Cannot add or update a child row: a foreign key constraint fails)
differ_key_sku_head = list(set(df_tt_sku['sku_head'].unique()) -
                           set(df_sku_head['id'].unique()))
print('Number of differences between df_tt_sku[sku_head] & df_sku_head[id]: {}'.format(
    len(differ_key_sku_head)))
df_differ_key_sku_head = pd.DataFrame(differ_key_sku_head, columns=['id'])
df_differ_key_sku_head['Type'] = empty_value
df_differ_key_sku_head['product'] = empty_value
df_sku_head = pd.concat(
    [df_sku_head, df_differ_key_sku_head], axis=0, ignore_index=True)

differ_key_brand_id = list(set(df_tt_sku['brand_id'].unique()) -
                           set(df_brand['id'].unique()))
print('Number of differences between df_tt_sku[brand_id] & df_brand[id]: {}'.format(
    len(differ_key_brand_id)))
df_differ_key_brand_id = pd.DataFrame(differ_key_brand_id, columns=['id'])
df_differ_key_brand_id['brand'] = empty_value
df_brand = pd.concat(
    [df_brand, df_differ_key_brand_id], axis=0, ignore_index=True)

differ_key_model_id = list(set(df_tt_sku['model_id'].unique()) -
                           set(df_model['id'].unique()))
print('Number of differences between df_tt_sku[model_id] & df_model[id]: {}'.format(
    len(differ_key_model_id)))
df_differ_key_model_id = pd.DataFrame(differ_key_model_id, columns=['id'])
df_differ_key_model_id['model'] = empty_value
df_model = pd.concat(
    [df_model, df_differ_key_model_id], axis=0, ignore_index=True)

differ_key_sku_tail_id = list(set(df_tt_sku['sku_tail_id'].unique()) -
                              set(df_sku_tail['id'].unique()))
print('Number of differences between df_tt_sku[sku_tail_id] & df_sku_tail[id]: {}'.format(
    len(differ_key_sku_tail_id)))
df_differ_key_sku_tail_id = pd.DataFrame(
    differ_key_sku_tail_id, columns=['id'])
df_differ_key_sku_tail_id['sku_tail'] = empty_value
df_sku_tail = pd.concat(
    [df_sku_tail, df_differ_key_sku_tail_id], axis=0, ignore_index=True)

# CSV produced before writing into database
df_tt_sku['sku_id'] = df_tt_sku.index + 1
assert quantity_Sum == df_tt_sku['quantity'].sum(
), '[WARNING] Total quantity is different between origin file and the file adjusted by ETL.'
print('df_tt_sku is: \n', df_tt_sku.head(21))
df_tt_sku.to_csv('./df_tt_sku_sample_ETL.csv', index=False, encoding='ANSI')

# Write records stored in a DataFrame to a SQL database
try:
    df_sku_head.to_sql(name='sku_head',
                       con=sqlengine,
                       index=False,
                       if_exists='append')

    df_brand.to_sql(name='brand',
                    con=sqlengine,
                    index=False,
                    if_exists='append')

    df_model.to_sql(name='model',
                    con=sqlengine,
                    index=False,
                    if_exists='append')

    df_sku_tail.to_sql(name='sku_tail',
                       con=sqlengine,
                       index=False,
                       if_exists='append')

    df_tt_sku[['sku_id', 'sku', 'quantity', 'created_date',
               'sku_noplus', 'sku1', 'sku2', 'nchar', 'sku_num', 'ndigit',
               'sku_head', 'sku_tail_id', 'brand_id', 'model_id', 'design_id']].to_sql(name='tt_sku',
                                                                                       con=sqlengine,
                                                                                       index=False,
                                                                                       if_exists='append')

    print('Write data to DB Done!!!')

except Exception as Ex:
    print('[EXCEPTION] {}'.format(Ex))
