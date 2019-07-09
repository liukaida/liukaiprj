# encoding=utf8
# coding=utf8
import os
import xlwt

from apps.pypinyin.__init__ import pinyin

WORDS = u"""
我们,爸爸.难过 银行
我 我们、我的，我行.我行，我行，我行，我行
我（我们 我的 我行） 还有谁 中华人民共和国中华人民共和国中华人民共和国
我是谁， 谁是我
"""
MIN_CHARLEN = 2  # 最小单词长度
MAX_CHARLEN = 100  # 最大单词长度
ONE_ROW_MAX_CHAR = 15  # EXCEL中每行最多容纳的字符数
INIT_ROW = 1  # 首个字符所在行
INIT_COL = 0  # 首个字符所在列

REPLACECHAR = u"\n\r\d.,()，。（）　、"  # 这些字符视为空格

PINYIN_CELL_HEIGHT = 'font:height 108;'
PINYIN_CELL_WIDTH = None

CHAR_CELL_HEIGHT = 'font:height 216;'
CHAR_CELL_WIDTH = 256*3-100

SPACE_CELL_HEIGHT = None
SPACE_CELL_WIDTH = 256*3-100  # 256*1

borders1 = xlwt.Borders()  # Create borders
borders1.left = xlwt.Borders.THIN
borders1.right = xlwt.Borders.DASHED
borders1.top = xlwt.Borders.THIN
borders1.bottom = xlwt.Borders.DASHED
style1 = xlwt.XFStyle()  # Create style
style1.borders = borders1  # Add borders to style

borders2 = xlwt.Borders()  # Create borders
borders2.left = xlwt.Borders.DASHED
borders2.right = xlwt.Borders.THIN
borders2.top = xlwt.Borders.THIN
borders2.bottom = xlwt.Borders.DASHED
style2 = xlwt.XFStyle()  # Create style
style2.borders = borders2  # Add borders to style

borders3 = xlwt.Borders()  # Create borders
borders3.left = xlwt.Borders.THIN
borders3.right = xlwt.Borders.DASHED
borders3.top = xlwt.Borders.DASHED
borders3.bottom = xlwt.Borders.THIN
style3 = xlwt.XFStyle()  # Create style
style3.borders = borders3  # Add borders to style

borders4 = xlwt.Borders()  # Create borders
borders4.left = xlwt.Borders.DASHED
borders4.right = xlwt.Borders.THIN
borders4.top = xlwt.Borders.DASHED
borders4.bottom = xlwt.Borders.THIN
style4 = xlwt.XFStyle()  # Create style
style4.borders = borders4  # Add borders to style

tall_style = xlwt.easyxf(CHAR_CELL_HEIGHT)

'''
May be: NO_LINE 无线, THIN 细实线, MEDIUM 中粗实现, DASHED 虚线, DOTTED, THICK粗实线, DOUBLE 双划线,
HAIR 点线, MEDIUM_DASHED 粗虚线, THIN_DASH_DOTTED 细点划线, MEDIUM_DASH_DOTTED 中点划点,
THIN_DASH_DOT_DOTTED 细双点划线, MEDIUM_DASH_DOT_DOTTED 中双点划线, SLANTED_MEDIUM_DASH_DOTTED 倾斜中粗点划线,
or 0x00 through 0x0D.
# '''
# borders.left_colour = 0x90 # 边框上色
# borders.right_colour = 0x90
# borders.top_colour = 0x90
# borders.bottom_colour = 0x90

def set_char_cell_style(worksheet, x, y, char='', style=None, height=CHAR_CELL_HEIGHT, width=CHAR_CELL_WIDTH):
    # 设置单元格的宽高和字符
    if style:
        worksheet.write(x, y, char, style)  # row, col, content
    else:
        worksheet.write(x, y, char)

    if width:
        worksheet.col(y).width = width

    if height:
        # tall_style = xlwt.easyxf(height) # 36pt,类型小初的字号
        worksheet.row(x).set_style(tall_style)


def set_char_bord(worksheet, x, y, islast=False, onechar=''):
    # 设置文字边框，文字由4个单元格组成

    set_char_cell_style(worksheet, x, y, onechar, style1)  # row, col, content
    set_char_cell_style(worksheet, x, y+1, '', style2)  # row, col, content
    set_char_cell_style(worksheet, x+1, y, '', style3)  # row, col, content
    set_char_cell_style(worksheet, x+1, y+1, '', style4)  # row, col, content

    # 如果是最后一个字符，需要加一个空列
    if islast:
        set_char_cell_style(worksheet, x, y+2, '', None, SPACE_CELL_HEIGHT, SPACE_CELL_WIDTH)  # row, col, content

    return


def set_word(worksheet, x, y, pinyinstr, charlen, hanzi):
    # 写一个词和后面的空列
    # worksheet.write(x, y, pinyinstr)
    set_char_cell_style(worksheet, x, y, char=pinyinstr, style=None, height=CHAR_CELL_HEIGHT, width=CHAR_CELL_WIDTH)
    for i in range(charlen):
        islast = False
        if i == charlen-1:
            islast = True

        onechar = hanzi[i] if hanzi else ''
        set_char_bord(worksheet, x+1, y+2*i, islast, onechar)
    pass


def get_pinyin_str(word):
    # 获取当前字符串的拼音字符串
    result = []
    word_pinyin = pinyin(word)
    for each_word_pinyin in word_pinyin:
        for each_char_pinyin in each_word_pinyin:
            result.append(each_char_pinyin)
    return ' '.join(result)


def split_long_word(word):
    # 将超过一行长度的字符截成刚好一行长度，否则不处理
    result = []
    word_len = len(word)
    if word_len > ONE_ROW_MAX_CHAR:
        for i in range(word_len/ONE_ROW_MAX_CHAR + 1):
            result.append(word[i*ONE_ROW_MAX_CHAR:(i+1)*ONE_ROW_MAX_CHAR])
    else:
        result.append(word)
    return result


# def set_pos_word(worksheet, x, y, pinyinstr, charlen):
#     set_word(quizworksheet, 0, 0, 'ni hao', 2)


def get_pinyin_excel(words=WORDS, excel_filename=r'temp/quiz.xls', has_hanzi=None):
    # 获取excel
    if os.path.exists(excel_filename):
        try:
            os.remove(excel_filename)
        except Exception as e:
            print u'请先关闭打开的excel,注意自行保存你需要的内容！'
            raise Exception(u'请先关闭打开的excel,注意自行保存你需要的内容！')
            # exit(-1)
        print 'removed'

    quizworkbook = xlwt.Workbook()  # Create workbook
    quizworksheet = quizworkbook.add_sheet('My sheet')  # Create worksheet

    # 先将文字去掉分隔字符
    new_word_list = []
    for each_char in REPLACECHAR:
        words = words.replace(each_char, ' ')
    # print words

    # 通过空格拆分，并去掉长度不满足要求的字符
    words_list = words.split(' ')
    for each_word in words_list:
        if MIN_CHARLEN <= len(each_word) <= MAX_CHARLEN:
            # 先检查文字是否超出一行的长度
            new_word_list.extend(split_long_word(each_word))

    print new_word_list

    # 初始位置
    curx = INIT_ROW
    cury = INIT_COL
    cur_index = 0
    cur_row_char_len = 0
    for each_word in new_word_list:
        each_word_pinyin = get_pinyin_str(each_word)
        each_word_len = len(each_word)
        hanzi = each_word if has_hanzi else ''
        # print curx, cury, each_word, each_word_pinyin, each_word_len
        set_word(quizworksheet, curx, cury, each_word_pinyin, each_word_len, hanzi)

        # 计算下一个字符位置
        cur_row_char_len += each_word_len
        next_word_len = 0
        if cur_index < len(new_word_list) - 1:
            next_word_len = len(new_word_list[cur_index+1])
        if cur_row_char_len + next_word_len <= ONE_ROW_MAX_CHAR:
            cury = cury + each_word_len * 2 + 1
        else:
            curx = curx + 4
            cury = INIT_COL
            cur_row_char_len = 0

        cur_index += 1

    quizworkbook.save(excel_filename)
