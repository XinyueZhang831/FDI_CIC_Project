import io
import csv

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
import time


def extract_text_from_pdf(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()
        split_array(text)
    converter.close()
    fake_file_handle.close()

    if text:
        return text

def split_array(text):
    print(text)
    array1 = text.split()
    print(array1)
    first_clean(array1)


def first_clean(array1): #clean all page number
    array2 = []
    for item in array1:
        if item.isdigit() == False:
            array2.append(item)
    split_parentheses(array2)

def split_parentheses(array1):
    array2 = []

    for i in range(len(array1)):
        if len(array1[i])>10:
            if array1[i][3] == '.' :
                text = array1[i].split('.')
                text1 = text[0] + '.'
                array1.pop(i)
                array1.insert(i, text1)
                array1.insert(i+1, text[1])
    num_character = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
    for item in array1:
            if (len(item) > 3) & (item[0] == '（') & (item[1] in num_character):
                if (item[0] == '（') & (item[2] == '）'):
                    item1 = item[0:3]
                    item2 = item[3:]
                    array2.append(item1)
                    array2.append(item2)
                if (item[0] == '（') & (item[3] == '）'):
                    item1 = item[0:4]
                    item2 = item[4:]
                    array2.append(item1)
                    array2.append(item2)
                if (item[0] == '（') & (item[4] == '）'):
                    item1 = item[0:5]
                    item2 = item[5:]
                    array2.append(item1)
                    array2.append(item2)
            else:
                array2.append(item)
    solve_symbol(array2)

def solve_symbol(array1):
    num_character = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
    array2 = []
    for item in array1:
        if (item[0] in num_character)& (item[1] == '、'):
                item1 = item[0:2]
                item2 = item[2:]
                array2.append(item1)
                array2.append(item2)
        elif len(item) >2:
            if (item[0] in num_character) & (item[1] in num_character) & (item[2] == '、'):
                item1 = item[0:3]
                item2 = item[3:]
                array2.append(item1)
                array2.append(item2)
            else:
                array2.append(item)

        else:
                array2.append(item)
    solve_split_page(array2)


def solve_split_page(array1):
    array2 = []
    num_character = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
    for item in array1:
        if len(array2) > 0:
            check = array2[len(array2) - 1]
            if (item[0] > u'\u4e00') & (item[0] < u'\u9fff') & (item[1] != '、') & ((item[0] in num_character)==False):
                    if (check[len(check)-1] > u'\u4e00') & (check[len(check)-1] < u'\u9fff'):
                        item1 = array2[len(array2) - 1] + item
                        del array2[len(array2) - 1]
                        array2.append(item1)
                    elif check[len(check)-1].isalpha():
                        item1 = array2[len(array2) - 1] + item
                        del array2[len(array2) - 1]
                        array2.append(item1)
                    elif (check[len(check)-1] == '、') & (len(check) >5):
                        item1 = array2[len(array2) - 1] + item
                        del array2[len(array2) - 1]
                        array2.append(item1)
                    else:
                        array2.append(item)
            elif ((item[0]in num_character) == False) & (check[len(check)-1] == ')'):
                item1 = array2[len(array2) - 1] + item
                del array2[len(array2) - 1]
                array2.append(item1)
            else:
                array2.append(item)
        else:
            array2.append(item)
    solve_missing_space(array2)

def solve_missing_space(array1):
    array2 = []
    for item in array1:
        if len(array2) > 1:
            if len(item) > 4:
                check = array2[len(array2) - 1]
                if (check[0].isdigit()) & (item[0].isdigit()):
                    array2.append(item)
                elif (check[0].isdigit() == False) & (item[0].isdigit()):
                    i = 0
                    while i < len(item)-1:
                        if item[i] == '.':
                            item1 = item[0:i+1]
                            item2 = item[i+1:]
                            array2.append(item1)
                            array2.append(item2)
                        i +=1
                else:
                    array2.append(item)
            else:
                array2.append(item)
        else:
            array2.append(item)
    #print(array2)
    solve_too_many_space(array2)

    #write_to_csv(array2)

def solve_too_many_space(array1):
    array2 = []
    num_character = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
    for item in array1:
        if len(array2) > 1:
            check = array2[len(array2)-1]
            if len(item)>4:
                if (item[0] == '(') & ((item[2] in num_character)== False) & (check[len(check)-1] > u'\u4e00') & (check[len(check)-1] < u'\u9fff'):
                    item1 = array2[len(array2) - 1] + item
                    del array2[len(array2) - 1]
                    array2.append(item1)
                elif (item[0] == '（') & ((item[2] in num_character)== False) & (check[len(check)-1] > u'\u4e00') & (check[len(check)-1] < u'\u9fff'):
                    item1 = array2[len(array2) - 1] + item
                    del array2[len(array2) - 1]
                    array2.append(item1)
                else:
                    array2.append(item)
            else:
                array2.append(item)
        else:
            array2.append(item)
    combine_parenthese_text(array2)

    #write_to_csv(array2)
def combine_parenthese_text(array1):
    array2 = []
    num_character = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
    for item in array1:
        if len(array2) > 1:
            check = array2[len(array2) - 1]
            if (check[len(check) - 1] == ')') & ((check[len(check) - 2] in num_character ) == False) & (item[0] > u'\u4e00') & (item[0] < u'\u9fff'):
                item1 = array2[len(array2) - 1] + item
                del array2[len(array2) - 1]
                array2.append(item1)
            else:
                array2.append(item)
        else:
            array2.append(item)

    write_to_csv(array2)

def write_to_csv(array2):
    print(array2)
    counter = 0
    num_character = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
    with open('2007_catalog.csv', 'w', encoding="utf-8") as csvfile:
        spamwriter = csv.writer(csvfile)
        while counter < len(array2) - 1:
            check = array2[counter]
            if (check[0] in num_character) | (check[0].isdigit()) |(check[1] in num_character):
               #print(array2[counter] + ',' + array2[counter + 1] + ',')
                spamwriter.writerow([array2[counter]] + [array2[counter + 1]] )
                counter += 2
            else:
                spamwriter.writerow([array2[counter]])
                counter +=1




extract_text_from_pdf('/Users/xinyue/PycharmProjects/cic_peoject/2007/2007_catalog.pdf')