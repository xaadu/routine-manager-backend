from typing import List
from docx import Document
from docx.table import Table


def extractSub(sub: str, lecturers: dict) -> dict:
    sub = sub.replace(']', '').split('[')
    if len(sub) == 3:
        data = {
            #'break': False,
            'lecturer': lecturers.get(sub[0], sub[0]),
            'lecturer_code': sub[0],
            'course_code': sub[2],
        }
    else:
        data = {
            #'break': True,
            'lecturer': '',
            'lecturer_code': '',
            'course_code': '',
        }
    return data


def generate(table: Table, data: list, times: list, lecturers: dict):
    for i, row in enumerate(table.rows):
        if i==0:
            continue
        elif i==1:
            times = [cell.text.strip() for cell in row.cells][3:]
        else:
            cells = [cell.text.strip() for cell in row.cells]
            day, sem, sec, subjects = cells[0].lower(), cells[1][:1], cells[2], cells[3:]
            sec = sec.split(',')
            if len(sec)!=2:
                continue
            sec, room = sec[0].strip()[8:], sec[1].strip()[2:]

            for sub in subjects:
                sub = sub.replace(']', '').split('[')
                if len(sub) == 3:
                    batch = sub[1].split('B')[0]
                    break
            else:
                batch = ''
            
            subjects = [{'time': tim, **extractSub(sub, lecturers)} for tim, sub in zip(times, subjects)]

            sem_index = next((i for i, item in enumerate(data) if item["semester"] == sem), None)
            if sem_index == None:
                data.append({
                        'batch': batch,
                        'semester': sem,
                        'sections': list()
                    })
                sem_index = len(data)-1
            
            if data[sem_index].get("batch") == "" and batch != "":
                data[sem_index].update({'batch': batch})
            
            sec_index = next((i for i, item in enumerate(data[sem_index]["sections"]) if item["section"] == sec), None)
            if sec_index == None:
                data[sem_index]["sections"].append({
                        'section': sec,
                        'room': room,
                        'days': list()
                    })
                sec_index = len(data[sem_index]["sections"])-1

            data[sem_index]["sections"][sec_index]["days"].append({
                                                            'day': day,
                                                            'courses': subjects
                                                        })
    return data, times


def extract_lecturers(table: Table, lecturers: dict) -> dict:
    for row in table.rows:
        for cell in row.cells:
            text = cell.text.replace('–', '-').split('-')
            if len(text) == 2:
                lecturers.update({text[0].strip(): text[1].strip()})

    return lecturers


def get_routine_data(filename: str) -> dict:
    data, times, lecturers = list(), list(), dict()

    document = Document(filename)
    tables = document.tables

    for table in tables:
        if len(table.columns)==3 or len(table.columns)==4:
            for row in table.rows:
                for cell in row.cells:
                    text = cell.text.replace('–', '-').split('-')
                    if len(text)==2 and len(text[1].split(' '))>1:
                        lecturers = extract_lecturers(table, lecturers)
                    break
                break

    for table in tables:
        if len(table.columns)==9:
            data, times = generate(table, data, times, lecturers)

    return data
