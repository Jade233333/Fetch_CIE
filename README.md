# Fetch_CIE

Use python to download CIE past papers from cie.craft.cn

## Installation

Clone the repository

```
git clone https://github.com/Jade233333/Fetch_CIE.git
```

Install the requirements

```
pip install -r requirements.txt
```

## Use

Write configuration file in `yaml` to filter past papers to download.
Example file: config.yaml

Code: exam code which you can find on the official website of CIE
Season: `w` for winter;`s` for summer; `m` for march(Indian paper)
Year: last two digits of a year, eg. `23` for 2023
Paper type: `qp` for question paper; `ms` for mark scheme; `er` for exam report; `gt` for grade thresholds
Component Number: each syllabus' exams have different components such as multiple choice, and structure questions.
Time zone: time zone numbers are from 1 to 6, you can find your time zone number on [official website](https://www.cambridgeinternational.org/exam-administration/cambridge-exams-officers-guide/phase-1-preparation/timetabling-exams/administrative-zone/) , and find your respective exam [timetable](https://www.cambridgeinternational.org/exam-administration/cambridge-exams-officers-guide/phase-1-preparation/timetabling-exams/exam-timetables/)

Run the python file

```
python fetch_CIE.py -d /path/to/download -c /path/to/config/file
```

## To-do list

- [] generate config for failed papers
