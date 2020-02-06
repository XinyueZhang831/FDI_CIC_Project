import pandas as pd
import re

def read_in_file(path):
    original_file = pd.read_csv(path, skiprows=3, header=None)
    sub_original = original_file
    sub_original = sub_original.rename(columns={0: 'output_file'})
    sub_original = sub_original.rename(columns={1: 'content'})
    sub_original = sub_original.dropna()
    sub_original = sub_original.reset_index(drop=True)
    print(sub_original)
    result, split_list = find_all_parenthesis(sub_original)
    #result = add_industry(result)
    #result = split_item_by_symbol(result)
    result = replace_parentheses(result, split_list)
    result.to_csv('/Users/xinyue/PycharmProjects/cic_project/2007/2007_catalog.csv')


def find_all_parenthesis(df):
    text_list_for_split = []
    for i,r in df.iterrows():
        text= re.findall('\（\s?(.+?)\s?\）', r['content'])
        text_list = []

        for j in text:
            if ('中外' in j) |('中方' in j) |('外资' in j) |('合资' in j) |('合作' in j):#if any new key words, update here
                text_list.append(j)
                if (j in text_list_for_split) == False:
                    text_list_for_split.append('（' +j+ '）')
        df.at[i, 'restriction'] = (' ').join(text_list)
    return df, text_list_for_split

def add_industry(df):
    char_list = ['一、','二、','三、','四、','五、','六、','七、','八、','九、','十、','十一、','十二、','十三、','十四、','十五、','十六、']
    begin_char = ''
    list_of_index = []
    list_of_industry = []
    for i,r in df.iterrows():
        if (r['output_file'] in char_list) & (r['output_file'] != begin_char):
            sub_df_index_begin = i
            industry = r['content']
            begin_char = r['output_file']
            list_of_index.append(sub_df_index_begin)
            list_of_industry.append(industry)
    new_df = pd.DataFrame()
    for i in range(len(list_of_index)):
        if i < len(list_of_index)-1:
            partial_df = df.iloc[list_of_index[i]:list_of_index[i+1], :]
            partial_df['industry'] = list_of_industry[i]
            new_df = new_df.append(partial_df)
        else:
            partial_df = df.iloc[list_of_index[i]:, :]
            partial_df['industry'] = list_of_industry[i]
            new_df = new_df.append(partial_df)
    return new_df

def split_item_by_symbol(df):
    for i,r in df.iterrows():
        if '：'in r['content']:
            df.at[i,'group'] = r['content'].split('：')[0]
            df.at[i,'sub_content'] = r['content'].split('：')[1]
        else:
            df.at[i, 'group'] = r['content']
    return df


def replace_parentheses(df, split_list):
    df['sub_content'] = df['content']
    for i in split_list:
        #df['content'] = df['content'].str.replace(i, '')
        df['sub_content'] = df['sub_content'].str.replace(i, '')
    return df





path = '/Users/xinyue/PycharmProjects/cic_project/2007/2007_catalog_base.csv'
read_in_file(path)