import pandas as pd
import re


def read_in_file():
    catalog = pd.read_csv('/Users/xinyue/PycharmProjects/cic_peoject/2002/2002_original.csv')
    print(catalog)
    clean_catalog_number = clean_number(catalog)
    clean_catalog_number = first_modeify(clean_catalog_number)
    clean_catalog_number = second_modeify(clean_catalog_number)
    #clean_catalog_number = send_to_ninth_clean(clean_catalog_number)
    col = ['output_file', 'content', 'restriction','sub_content']
    clean_catalog_number = clean_catalog_number[col]
    clean_catalog_number.to_csv('2002_catalog.csv')




def clean_number(catalog):
    catalog['output_file'] = ''
    catalog['content'] = ''
    chinese_char_2 = ['一、','二、','三、','四、','五、','六、','七、', '八、', '九、', '十、']
    for i,r in catalog.iterrows():
        if '.' in r['外商投资产业指导目录 ']:
            text =  r['外商投资产业指导目录 '].split('.')
            text1 = text[0]
            text2 = ('').join(text[1:])
            text2 = text2.replace('　', '')
            catalog.at[i, 'output_file'] = text1
            catalog.at[i, 'content'] = text2

        elif r['外商投资产业指导目录 '][0] == '（':
            text = r['外商投资产业指导目录 '].split('）')
            text1 = text[0]
            text2 = ('').join(text[1:])
            text2 = text2.replace('　', '')
            catalog.at[i, 'output_file'] = text1 + ' )'
            catalog.at[i, 'content'] = text2
            #for item_1 in chinese_char_1:
                #if item_1 in r['外商投资产业指导目录 ']:
        else:
            catalog.at[i, 'output_file'] = r['外商投资产业指导目录 ']
            catalog.at[i, 'content'] = ''


        for item_2 in chinese_char_2:
            if item_2 in r['外商投资产业指导目录 ']:
                text = r['外商投资产业指导目录 '].split('、')
                text1 = text[0]
                text2 = ('').join(text[1:])
                text2 = text2.replace('　', '')
                catalog.at[i, 'output_file'] = text1+'、'
                catalog.at[i, 'content'] = text2
    return catalog


def first_modeify(original_file):
    index_list = []
    for i,r in original_file.iterrows():
        if r['output_file'] == '三、':
            index_list.append(i)
        if r['output_file'] == '四、':
            index_list.append(i)
    m_only = pd.DataFrame()
    i = 0
    while i < len(index_list):
        if i != len(index_list)-1:
            m_only = m_only.append(original_file.iloc[index_list[i]:index_list[i+1],:])
            i=i+2
    m_only = m_only.reset_index(drop=True)
    return m_only

def second_modeify(m_only):
    text_list_for_split = []
    for i,r in m_only.iterrows():
        text= re.findall('\（\s?(.+?)\s?\）', r['content'])
        text_list = []
        for j in text:
            if ('中外' in j) |('中方' in j) |('外资' in j) |('合资' in j) |('合作' in j):#if any new key words, update here
                text_list.append(j)
                if (j in text_list_for_split) == False:
                    text_list_for_split.append('（' +j+ '）')
        m_only.at[i, 'restriction'] = (' ').join(text_list)
    m_only['sub_content'] = m_only['content']
    for i in text_list_for_split:
        m_only['sub_content'] = m_only['sub_content'].str.replace(i, '')
    return m_only

def send_to_ninth_clean(catalog):
    index_list = []
    catalog['support'] = 0
    catalog['limited'] = 0
    catalog['forbid'] = 0
    for i, r in catalog.iterrows():
        if r['content'] == '制造业 ':
            index_list.append(i)
    for ind, row in catalog.iterrows():
        if (ind>=index_list[0])&(ind<index_list[1]):
            catalog.at[ind, 'support'] = 1
        if (ind>=index_list[1])&(ind<index_list[2]):
            catalog.at[ind, 'limited'] = 1
        if ind >= index_list[2]:
            catalog.at[ind, 'forbid'] = 1
    return catalog





read_in_file()