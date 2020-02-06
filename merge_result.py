import pandas as pd


def allfiles():
    df_re = pd.DataFrame()
    file = ['/Users/xinyue/PycharmProjects/cic_peoject/hand_in/merge_catalog/2007_catalog.csv', '/Users/xinyue/PycharmProjects/cic_peoject/hand_in/merge_catalog/1997_catalog.csv', '/Users/xinyue/PycharmProjects/cic_peoject/hand_in/merge_catalog/2002_catalog.csv']
    result_file = ['/Users/xinyue/PycharmProjects/cic_peoject/hand_in/merge_catalog/2007_catalog_result.xlsx', '/Users/xinyue/PycharmProjects/cic_peoject/hand_in/merge_catalog/1997_catalog_result.xlsx', '/Users/xinyue/PycharmProjects/cic_peoject/hand_in/merge_catalog/2002_catalog_result.xlsx']
    for f,re in zip(file,result_file):
        year = f.split('/')[-1][:4]
        part = read_in(f, re, year)
        df_re = df_re.append(part)
    df_re = df_re.rename(columns={'restriction': 'ownership'})
    df_re.to_csv('/Users/xinyue/PycharmProjects/cic_peoject/hand_in/merge_catalog/Result/Result.csv')


def read_in(file, result_file,year):
    if '2007' in result_file:
        df_result = pd.read_excel(result_file, skiprows=3, header=None)
        df_result = df_result.rename(columns={0: 'output_file'})
        df_result = df_result.rename(columns={1: 'content'})
        df_result = df_result.rename(columns={2: 'cic'})
    else:
        df_result = pd.read_excel(result_file, skiprows=1, header=None)
        df_result=df_result.drop(columns=[0])
        df_result = df_result.rename(columns={1: 'output_file'})
        df_result = df_result.rename(columns={2: 'sub_content'})
        df_result = df_result.rename(columns={3: 'cic'})
    key_column = df_result.columns[1]
    df_result=df_result.reset_index()
    df_result = df_result.drop(columns=['output_file'])
    df = pd.read_csv(file)
    df=df.drop(columns=['Unnamed: 0'])
    df= df.reset_index()
    print(df.columns)
    df_total = merge_file(df_result,df,key_column)
    final = reshape(df_total)
    print(final.columns)
    col = ['index', 'output_file', 'content', 'sub_content', 'restriction', 'cic', 'CIC']
    final = final[col]
    final['Year'] = year
    return final


def merge_file(df_result,df,key_column):
    df = df.merge(df_result, on= [key_column,'index'])
    return df

def reshape(df_total):
    df_final = pd.DataFrame()
    for i,r in df_total.iterrows():
        sub_df= df_total.loc[i]
        if type(r['cic']) != float:
            text = r['cic'].replace('[','')
            text = text.replace(']', '')
            text = text.split(',')
            sub_df = expand(sub_df, text)
            df_final= df_final.append(sub_df)
        else:
            df_final = df_final.append(sub_df)
    return df_final


def expand(df,text):
    df_expand = pd.DataFrame()
    for i in text:
        df['CIC'] = i
        df_expand=df_expand.append(df)
    return df_expand


# 2007 1997
# read_in(file, result_file)
allfiles()