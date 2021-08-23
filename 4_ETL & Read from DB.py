# -*- coding: utf-8 -*-
from lib import SQLAlchemy
from lib import Email_SMTP
from email.header import Header
import pandas as pd
import numpy as np
import os


# ---------------------------------------------------------------------------------------------------- #
# Import Data and Function
# ---------------------------------------------------------------------------------------------------- #
# Function - Database
sqlalchemy = SQLAlchemy(Database_Type='mysql',
                        User='###your username###',
                        Pwd='###your password###',
                        Host='###your host###',
                        Port='###your port###',
                        Database='###your database name###')

# Function - Database
email_smtp = Email_SMTP(Host='smtp.gmail.com',
                        Port=465,
                        User='###your sender email###',
                        Pwd='###your password###')

# df_tt_sku_sample
df_tt_sku = pd.read_csv('./df_tt_sku_sample.csv')
quantity_Sum = df_tt_sku['quantity'].sum()


# ---------------------------------------------------------------------------------------------------- #
# 建構資料庫連線，取出資料計算
# ---------------------------------------------------------------------------------------------------- #
sqlengine = sqlalchemy.create_engine()

# Get data from database
sql = """
    SELECT tt.sku, tt.quantity, tt.created_date,
            sh.Type, sh.product,
            br.brand,
            md.model,
            st.sku_tail

    FROM tt_sku AS tt
    LEFT JOIN sku_head AS sh
    ON tt.sku_head=sh.id

    LEFT JOIN brand AS br
    ON tt.brand_id=br.id

    LEFT JOIN model AS md
    ON tt.model_id=md.id

    LEFT JOIN sku_tail AS st
    ON tt.sku_tail_id=st.id
"""

df_tt_sku_db = pd.read_sql_query(sql, sqlengine)
assert quantity_Sum == df_tt_sku_db['quantity'].sum(
), '[WARNING] Total quantity is different between origin file and database.'

# Group by brand
df_cal_brand = df_tt_sku_db.groupby(
    by=['brand']).sum().groupby(level=[0]).cumsum()
assert quantity_Sum == df_cal_brand['quantity'].sum(
), '[WARNING] Total quantity is different between origin file and quantity report(by brand).'
filename_brand = os.path.abspath('./quantity report_by brand.csv')
df_cal_brand.to_csv(filename_brand,
                    index=True, encoding='ANSI')

# Group by created_date
df_cal_created_date = df_tt_sku_db.groupby(
    by=['created_date']).sum().groupby(level=[0]).cumsum()
assert quantity_Sum == df_cal_created_date['quantity'].sum(
), '[WARNING] Total quantity is different between origin file and quantity report(by created_date).'
filename_created_date = os.path.abspath(
    './quantity report_by created_date.csv')
df_cal_created_date.to_csv(filename_created_date,
                           index=True, encoding='ANSI')

# Group by sku_tail & brand & Type & product & model & sku & created_date
df_cal_multi = pd.pivot_table(df_tt_sku_db, index=['sku_tail', 'brand', 'Type', 'product', 'model', 'sku', 'created_date'], values=[
    'quantity'], aggfunc={'quantity': np.sum}, margins=True)
assert quantity_Sum == (df_cal_multi['quantity'].sum(
))/2, '[WARNING] Total quantity is different between origin file and quantity report(by multiple key).'
filename_multi = os.path.abspath(
    './quantity report_by sku_tail & brand & Type & product & model & sku & created_date.csv')
df_cal_multi.to_csv(filename_multi,
                    index=True, encoding='ANSI')


# ---------------------------------------------------------------------------------------------------- #
# 自動寄送計算結果報表
# ---------------------------------------------------------------------------------------------------- #
email_content = """<html>
                        <head>
                            <meta name="viewport" content="width=device-width, initial-scale=1">
                        </head>
                        <body>
                            <div>
                                <p style="font-size: 14px; line-height: 20px;">Hello,</p>
                                <p>&nbsp;</p>
                                <p style="font-size: 14px; line-height: 16px;">Attachments are Quantity Reports grouping by </p>
                                <ul style="font-size: 14px; line-height: 16px;">
                                　<li>brand</li>
                                　<li>created_date</li>
                                　<li>sku_tail & brand & Type & product & model & sku & created_date</li>
                                </ul>
                                <p style="font-size: 14x; line-height: 16px;">Should you have any questions, please feel free to contact me.</p>
                                <p style="font-size: 14px; line-height: 16px;">Thank you.</p>
                                <p>&nbsp;</p>
                                <p style="font-size: 14px; line-height: 16px;">Best Regards</p>
                            </div> 
                            <p>--</p>
                            </div>
                        </body>
            </html>"""

email_smtp.Send(send_subject=Header('[Report] Quantity Reports', 'utf-8'),
                send_from='###your sender email###',
                send_to=['###your receiver email###'],
                send_cc=[''],
                send_bcc=[''],
                send_atta=[filename_brand,
                           filename_created_date, filename_multi],
                send_body=email_content)
