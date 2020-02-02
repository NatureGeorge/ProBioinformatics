import json as js
import re
from datetime import timedelta


target_format = '''
{
    "font_size":0.2,
    "font_color":"#FFFFFF",
    "background_alpha":0.5,
    "background_color":"#9C27B0",
    "Stroke":"none",
    "body":[]}
'''

pattern = re.compile(r'([0-9:\.]+)\s(.+)')
pattern2 = re.compile(r'([0-9:\.]+) --> ([0-9:\.]+)')


def convertStr2Second(timeStr, var=("hours", "minutes", "seconds"), sep=":"):
    namedTp = zip(var, timeStr.split(sep))
    return float(timedelta(**{time: float(data) for time, data in namedTp}).total_seconds())


def extractInfo(line):
    time, content = pattern.search(line).groups()
    return convertStr2Second(time), content


def extractTime(time_line: str):
    time_line = time_line.replace(',', '.')
    start, end = pattern2.search(time_line).groups()
    return convertStr2Second(start), convertStr2Second(end)


def beforeAfter(lines, data):
    before = next(lines)
    before_time, before_content = extractInfo(before)
    for line in lines:
        cur_time, cur_content = extractInfo(line)
        data['body'].append({'from': before_time, 'to': cur_time-.05, 'location': 2, 'content': before_content})
        before_time, before_content = cur_time, cur_content
    data['body'].append({'from': before_time, 'to': before_time+1,
                         'location': 2, 'content': before_content})


def threeLineGroup(lines, data):
    cur = 0
    for index, line in enumerate(lines):
        if (index + 1) % 4 == 0 and cur != 0:
            cur = 0
            yield start, end, content
        else:
            cur += 1
            if cur == 2:
                start, end = extractTime(line)
            elif cur == 3:
                content = line[:-1]


def main2(filePath, outFilePath):
    data = js.loads(target_format)
    with open(filePath, 'rt') as inFile:
        ob = threeLineGroup(inFile, data)
        data['body'] = [{'from': start, 'to': end, 'location': 2, 'content': content} for start, end, content in ob]
    with open(outFilePath, 'wt') as outFile:
        js.dump(data, outFile, indent=4)
        


def main(filePath, outFilePath):
    data = js.loads(target_format)
    with open(filePath, 'rt') as inFile:
        beforeAfter(inFile, data)
    with open(outFilePath, 'wt') as outFile:
        js.dump(data, outFile, indent=4)


if __name__ == '__main__':
    # r'C:\迅雷下载\A Model for Protein Design.txt'
    filePath = r'C:\Users\Nature\Downloads\Rama Ranganathan U Texas Southwestern Part 2 A Model for Protein Design.en.txt'
    main2(filePath, r'C:\迅雷下载\P2.bcc')
