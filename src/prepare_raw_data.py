import pandas as pd
import numpy as np
import os
import glob
from common.io import file_base, parent_dir, mkdir
import re
import os

# @todo add warning if file is missing (i.e., None)
# @todo clean out files such that features are in 1 and labels (i.e., y or professor rating) is in another (samename_label.csv)
#

def get_metadata(fname, class_type=('lecture', 'lab', 'seminar', 'recitation discussion')):

    fname = fname.replace("Full_","");
    str_split = fname.split('_')
    semester = str(str_split[1] + str_split[2][2:4]).lower()

    fparts = str_split[0].split('/')[-1].split('-')
    cid = fparts[0]
    cid = [cid.lower().replace(c, '') for c in class_type if c.lower() in str(cid).lower()]

    if len(cid) == 0:
        return None, None, None, None
    if (re.search("[0-9]{6}",cid[0])):
        course_id = cid[0][:-2]
        section = cid[0][-2:]
    else:
        course_id = cid[0]
        section = '01'

    name = fparts[1].lower()

    return course_id, semester, name, section


def get_scores(fpath):
    """

    :param fpath:
    :return:
    """
    #  parse table
    df_scorechart = pd.read_excel(fpath, skiprows=10, nrows=29)
    df_scorechart.drop(df_scorechart.columns[12:], axis=1)

    return df_scorechart


def parse_surveys(data_dir, output_dir):
    """

    :param data_dir:
    :param output_dir:
    :return:
    """
    survey_dirs = glob.glob(data_dir + '*')

    colleges = [str(d).replace(data_dir, '') for d in survey_dirs]

    for college in colleges:

        obin = output_dir + '/' + college + '/'
        mkdir(obin)

        inbin = data_dir + '/' + college + '/'

        survey_paths = glob.glob(inbin + '*.xls')
        for survey in survey_paths:

            course, semester, name, section = get_metadata(survey)
            if course is None:
                continue
            df_scores = get_scores(survey)

            course_dir = os.path.join(obin, course)
            if mkdir(course_dir):
                print('created {}'.format(course_dir))
            semester_dir = os.path.join(course_dir, semester)

            if mkdir(semester_dir):
                print('created {}'.format(semester_dir))

            fout = semester_dir + '/' + name + '_' + section + '_' + semester + '.csv'

            df_scores.to_csv(fout)



if __name__ == "__main__":
    fpath = '/Users/zackhillman/Documents/eece2300/FinalProject/termproject/data/raw/surveys-raw/camd/CINE233601Lecture-Blake-201840_Summer_1_2018-Ratings_summary_w_CRN.xls'

    data_dir = '/Users/zackhillman/Documents/eece2300/FinalProject/termproject/data/raw/surveys-raw/'
    output_dir = '/Users/zackhillman/Documents/eece2300/FinalProject/termproject/data/processed/surveys/'

    parse_surveys(data_dir, output_dir)


#
# dict_of_colleges = {}
# dict_of_files = {}
# for (dirpath, dirnames, filenames) in os.walk(data_dir):
#     list_of_files = []
#     college_ref = file_base(dirpath)
#     for filename in filenames:
#         if filename.endswith('.xls'):
#             dict_of_files[filename] = os.sep.join([dirpath, filename])
#             list_of_files.append(filename)
#     if len(list_of_files) > 0:
#         dict_of_colleges[college_ref] = list_of_files
# #  parse header
#
# for k, v in dict_of_colleges.items():
#     print('There are {} samples for {}'.format(k, len(dict_of_colleges[k])))
# # There are ccis samples for 254
# # There are camd samples for 54
# # There are dmsb samples for 174
# # There are coe samples for 280
#
# #parse init info
# df_initial = pd.read_excel(fpath, nrows=6)
#
# df_intiial_transposed = df_initial.T
#
# df_initial = df_intiial_transposed.iloc[:2]
#
# #print(df_initial)
#
#
#
# # parse averaged scores
# df_overall_raw = pd.read_excel(fpath, skiprows=40, nrows=1)
#
# # check if last column is Nan
# if str(df_overall_raw.columns[-1][:6]).lower() == 'unname':
#     df_overall_raw = df_overall_raw.drop(labels=df_overall_raw.columns[-1], axis=1)
#
# #print(df_overall_raw)
#
# df_overall = df_overall_raw.iloc[:, 3::]
# #print(df_overall)
#
# df_scorechart.to_json("/Users/zackhillman/Documents/eece2300/FinalProject/termproject/data/processed/1.txt")
#
# # stats (i.e. number of each type of survey)