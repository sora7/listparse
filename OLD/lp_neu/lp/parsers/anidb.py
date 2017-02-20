# mal.py
# ann.py
# wa.py
# and so on

# parse_person()
# parse_company()
# parse_mylist()
# parse_title()

import re
import os

from lp.containers import Title


def print_title(t):
    print('%6s | %4s | %4s | %-11s | %5s | %s' % (t.title_id, t.eps, t.year,
                                                  t.type, t.rating,
                                                  t.title_name))


def split_year(year_data):
    years = year_data.split(' - ')
    if len(years) == 2:
        return years
    return years[0], years[0]


def parse_company(txt):
    # decode the retarded unicode
    # txt_u = txt.decode('utf8')

    # extract major staff section
    sep1 = '<table id="stafflist"'
    sep2 = '</tbody></table>'
    major_staff = txt.split(sep1)[1]
    major_staff = major_staff.split(sep2)[0]

    name_re = re.compile('<td.*?class="name anime"><a href="(.*?aid=(\d*?))">(.*?)</a></td>')
    type_re = re.compile('<td.*?class="type">(.*?)</td>')
    # type_re = re.compile('<td[ ]rowspan="\d*?"[ ]class="type">(.*?)</td>')
    eps_re = re.compile('<td.*?class="eps">(\d*?)</td>')
    year_re = re.compile('<td.*?class="year">(.*?)</td>')
    rating_re = re.compile('<td.*?class="rating">(.*?)[ ]<')

    titles = []

    row_sep = '<tr id="staffid_'
    rows = major_staff.split(row_sep)

    # skip the first row (header)
    for row in rows[1:]:
        title = Title()

        if name_re.search(row):
            title_link, title_id, title_name = name_re.findall(row)[0]
            title.title_link = title_link
            title.title_id = title_id
            title.title_name = title_name

        if type_re.search(row):
            type_ = type_re.findall(row)[0]
            title.type = type_

        if eps_re.search(row):
            eps = eps_re.findall(row)[0]
            title.eps = eps

        if year_re.search(row):
            year = year_re.findall(row)[0]

            year_start, year_end = split_year(year)
            title.year = year_start
            title.year_end = year_end

        if rating_re.search(row):
            rating = rating_re.findall(row)[0]
            title.rating = rating

        titles.append(title)
        print_title(title)

    return titles


def parse_person(txt):
    sep1 = '<table id="characterlist"'
    sep2 = '</tbody></table>'
    major_staff = txt.split(sep1)[1]
    major_staff = major_staff.split(sep2)[0]

    # char_name_re = re.compile()

    rowspan_re = re.compile('<td rowspan="(\d*?)" class="thumb image">')

    name_re = re.compile('<td.*?class="name anime"><a href="(.*?aid=(\d*?))">(.*?)</a></td>')
    type_re = re.compile('<td.*?class="type">(.*?)</td>')
    eps_re = re.compile('<td.*?class="eps">(?:(\d*?)|(?:.*?(TBC).*?))</td>')
    year_re = re.compile('<td.*?class="year">(.*?)</td>')
    rating_re = re.compile('<td.*?class="rating">(.*?)[ ]<')

    titles = []

    row_sep = '<tr id="charid_'
    rows = major_staff.split(row_sep)

    for row in rows[1:]:
        rowspan = int(rowspan_re.findall(row)[0])
        for i in range(rowspan):
            title = Title()

            if name_re.search(row):
                title_link, title_id, title_name = name_re.findall(row)[i]
                title.title_link = title_link
                title.title_id = title_id
                title.title_name = title_name

            if type_re.search(row):
                type_ = type_re.findall(row)[i]
                title.type = type_

            if eps_re.search(row):
                eps, tbc = eps_re.findall(row)[i]
                if tbc == '':
                    title.eps = eps
                else:
                    title.eps = tbc

            if year_re.search(row):
                year = year_re.findall(row)[i]

                year_start, year_end = split_year(year)
                title.year = year_start
                title.year_end = year_end

            if rating_re.search(row):
                rating = rating_re.findall(row)[i]
                title.rating = rating
            titles.append(title)
            print_title(title)

    print(len(titles))
    return titles


def test():
    mj = 'AniDB.net  Person - Maeda Jun.htm'
    hk = 'AniDB.net  Person - Hanazawa Kana.htm'

    filename = mj
    curr = os.path.abspath(os.curdir)
    filepath = os.path.join(curr, 'lists', filename)

    with open(filepath, encoding='utf-8') as f:
        txt = f.read()


    # print('???')
    # print('???')
    # # print(txt[11100:11230])
    # # print(txt[0:len(txt)])
    # print(txt.encode('utf-8'))

    parse_company(txt)