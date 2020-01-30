"""Walks through a specified directory and gets the following file information for 
all nested subdirectories: 
['full_path', 'file_name', 'created', 'last_modify','last_access', 'size(mb)']
For all parent directories, the size of all subfolders are added up, and the date items 
reflect the max of the newest version of dates from any file at an arbitrary depth."""



import os
import time
import pandas as pd
import datetime
from tqdm import tqdm, trange
from tkinter import *
from tkinter import filedialog

def save_path():
    """

    :return:
    """
    title = "Where do you want to save the output?"
    return filedialog.asksaveasfilename(title=title, filetypes=(("xlsx files", "*.xlsx"), ("all files", "*.*")), defaultextension='.xlsx')


def get_path():
    """

    :return:
    """
    title = "Please choose a directory to walk."
    return filedialog.askdirectory(title=title)


def walk(filepath):
    """

    :param parent:
    :param logger:
    :return:
    """
    for root, _, fnames in os.walk(filepath):
        for f in fnames:
            yield get_file_stats(os.path.abspath(os.path.join(root, f)))


def walk_with_progress(filepath):
    """

    :param filepath:
    :return:
    """
    file_count = 0
    for _ in walk(filepath):
        file_count += 1

    data = []
    for f in tqdm(walk(filepath), total=file_count, unit='files'):
        data.append(f)

    return data


def convert_datetime(item):
    """

    :param item:
    :return:
    """
    final = datetime.datetime.strptime(time.ctime(item), "%a %b %d %H:%M:%S %Y")
    return final


def get_file_stats(file):
    """

    :param file:
    :return:
    """

    (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(file)
    mb_size = round((size/1000000), 2)
    a_time = convert_datetime(atime)
    m_time = convert_datetime(mtime)
    c_time = convert_datetime(ctime)
    path, clean_file = file.rsplit("\\", 1)

    return [path, clean_file, c_time, m_time, a_time, mb_size]


def filelist_to_df(data):
    """

    :param cwd:
    :param logger:
    :return:
    """

    headers = ['full_path', 'file_name',
               'created', 'last_modify',
               'last_access', 'size(mb)']

    df = pd.DataFrame([x for x in data], columns=headers)

    return df


def clean_df(df):
    """

    :param df:
    :return:
    """
    # create dictionary for groupby series to add together
    clean = {}
    clean['size(mb)'] = df.groupby('full_path')['size(mb)'].agg('sum').round(2)
    clean['last_access'] = df.groupby('full_path')['last_access'].max()
    clean['last_modify'] = df.groupby('full_path')['last_modify'].max()
    clean['created'] = df.groupby(['full_path'])['created'].max()

    # create the DataFrame
    out_df = pd.DataFrame(data=clean)

    # reset index from 'full_path'
    out_df.reset_index(inplace=True)

    # comment here
    tmp_df = out_df.set_index('full_path', drop=False).full_path.apply(
        lambda path: out_df.loc[out_df.full_path.str.startswith(path)].agg({'size(mb)': 'sum', 'last_access': 'max'})).reset_index()
    out_df.update(tmp_df)

    # sort by last access date
    out_df.sort_values(by=['last_access'], inplace=True)

    return out_df


def write_to_excel(df, sheet, writer, index=False, index_count=0):
    """
    Writes to an excel sheet via a dataframe and a Excel Writer object supplied
    as parameters.

    The excel sheet isn't saved until the .save method is called, but this method closes
    the writer object, disallowing any further writing to excel.
    :return: Writes the excel object to cache to be flushed in the main function
    """

    df.to_excel(writer, sheet_name=sheet, index=index)

    # worksheet object created to specifically work on
    worksheet = writer.sheets[sheet]

    # sets max column width per length of text in dataframe series
    # caps this length at 50
    if index:
        buf = index_count
        for n in range(0, index_count+1):
            worksheet.set_column(n, n, 50)
    else:
        buf = 0

    for idx, col in enumerate(df):  # loop through all columns
        series = df[col]
        max_len = max((
            series.astype(str).map(len, na_action='ignore').max(),  # len of largest item
            len(str(series.name))  # len of column name/header
            )) + 1  # adding a little extra space
        if max_len > 50:    # limiting max size of columns to 50
            max_len = 50
        worksheet.set_column(idx+buf, idx+buf, max_len)  # set column width



def main():
    # initialize tcl/tk interpreter then withdraw the window
    root = Tk()
    root.withdraw()

    # get filepath to walk
    filepath = get_path()

    # get filepath to save
    out_file = save_path()

    # walk the directory with tqdmp progress bar
    data = walk_with_progress(filepath)

    """create df for files and sort values via last accessed datetime
    an additional and separate df will be created and manipulated for folders from the original df"""
    file_df = filelist_to_df(data)
    file_df = file_df.sort_values(by=['last_access', 'full_path']).set_index(['full_path', 'file_name'])
    # create folder df
    folder_df = clean_df(file_df)

    # intialize writer object
    writer = pd.ExcelWriter(out_file,
                            engine='xlsxwriter',
                            options={'strings_to_urls': False})

    """write both dfs to excel cache then flush with .save().  index call for the file df
    because it is being written in a multi-index format and this wouldn't be preserved.
    The multi-index item doesn't format column widths properly."""
    write_to_excel(folder_df, 'FOLDER_STATS', writer)
    write_to_excel(file_df, 'FILE_STATS', writer, index=True, index_count=2)

    writer.save()


if __name__ == '__main__':
    main()
