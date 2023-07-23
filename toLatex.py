#-*-coding:utf-8 -*-
import csv
import json
import ast
import sys
import argparse

with open('name.json', 'r') as f:
    name_list = json.load(f)
keys = list(name_list.keys())
for key in keys:
    name_list[name_list[key].lower()] = name_list[key].lower()

def myLog(info, end='\n', file='tmp.txt'):
    f = open(file, "a")
    f.write(info)
    f.write(end)
    f.close()
        
def TSVLoader(file):
    with open(file, newline='') as tsvfile:
        tsvdata = csv.reader(tsvfile, delimiter='\t', quotechar='%')
        data, ct = [],[]
        for line in tsvdata:
            try: 
                data.append([line[1], line[2], line[3], line[4]])
            except:
                print(line)
                data.append([line[1], line[2], line[3], ''])
            ct.append(line[0])
    return data, ct

def printN(ct, name, time, location, file):
    try:
        name = name_list[name.lower()]
    except:
        if len(name) < 1 or name[0] == '?':
            name = '\\textit{\\color{white}   aaaaaaaaaaa}'
        else:
            print('<%s>not exist!, Input new name, <B/b> for blank, <enter> for ori name'%name)
            a = input()
            if len(a) > 1:
                name_list[name.lower()] = a
                with open('name.json', 'w') as f:
                    json.dump(name_list, f)
                name = a
            elif a in ['B', 'b']:
                name = '\\textit{\\color{white}   aaaaaaaaaaa}'
        #name = 'Not In List'
    ct = str(ct)
    while len(ct)<3:
        ct = '0'+ct
    myLog(ct, end=' ', file=file)
    myLog('\\fbox{\\begin{minipage}{2.0cm}\\fontsize{4}{5}\\selectfont\\centering', end=' ', file=file)
    myLog('\\textbf{\\textit{%s}} \\\\'%name, end=' ', file=file)
    myLog('%s \\\\'%time, end=' ', file=file)
    location = location.replace("\"", "")
    location = location.split(',')
    acc = 0
    st = ''
    for i in range(len(location)):
        if i == 0:
            if len(location[i])+1 > 18:
                st += location[i] + ','
                continue
        if acc + len(location[i])+1 > 18:
            st += ' '
            acc = 0
        acc += len(location[i])+1
        st += location[i] + ','
    myLog('%s \\\\'%st[:-1], end=' ', file=file)
    myLog('\\end{minipage}}', file=file)

def printNote(note, file):
    myLog('\\fbox{\\begin{minipage}{2.0cm}\\fontsize{4}{5}\\selectfont\\centering', end=' ', file=file)
    acc = 0
    st = ''
    note = note.replace('&','\&')
    note = note.replace("\"", "")
    note = note.split(',')
    for i in range(len(note)):
        if i == 0:
            if len(note[i])+1 > 18:
                st += note[i] + ','
                continue
        if acc + len(note[i])+1 > 18:
            st += ' '
            acc = 0
        acc += len(note[i])+1
        st += note[i] + ','
    myLog('%s \\\\'%st[:-1], end=' ', file=file)
    myLog('\\end{minipage}}', file=file)


def printList(info, file=None, outfile=None):
    if file is not None:
        with open(file,'r') as f:
            data= f.read()
            info = ast.literal_eval(data)
    e = 0
    for i in range(len(info)):
        if info[i][0] == 'newline':
            myLog('\n\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n', file=outfile)
            e = 0
            continue
        if info[i][0] == 'EOF':
            break
        try:
            note = info[i][3]
            if e % 6 == 5:
                myLog('', file=outfile)
                e = 0
        except:
            pass
        printN(i+1, info[i][0], info[i][1], info[i][2], outfile)
        e+=1
        try:
            note = info[i][3]
            if note[0] == 'x' or note[0] == 'X':
                s=note.split(',')[0][1:]
                s=(int)(s)
                for _ in range(s-1):
                    printN(i+1, info[i][0], info[i][1], info[i][2], outfile)
                    e+=1
            else:
                printNote(note, outfile)
                e+=1
        except:
            pass            
        if e % 5 ==0:
            myLog('', file=outfile)
    myLog('\n\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n', file=outfile)
        
def printTSV(file, outfile):
    e = 0
    info, ct = TSVLoader(file)
    for i in range(len(info)):
        if info[i][0] == 'newline':
            myLog('\n\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n', file=outfile)
            e = 0
            continue
        if len(info[i][3]) > 0:
            if e % 6 == 5:
                myLog('', file=outfile)
                e = 0
        printN(ct[i], info[i][0], info[i][1], info[i][2], outfile)
        e+=1
        if len(info[i][3]) > 0:
            note = info[i][3]
            if note[0] == 'x' or note[0] == 'X':
                s=note.split(',')[0][1:]
                s=(int)(s)
                for _ in range(s-1):
                    printN(ct[i], info[i][0], info[i][1], info[i][2], outfile)
                    e+=1
            else:
                printNote(info[i][3], outfile)
                e+=1
        if e % 5 ==0:
            myLog('', file=outfile)
    myLog('\n\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n', file=outfile)
    
if __name__ == '__main__':
    d={}
    parser = argparse.ArgumentParser()
    parser.add_argument('--tsv', type=str, default='', help="--tsv <name.*sv> -o <name.txt> #split by tab or |")
    parser.add_argument('--txt', type=str, default='', help="--txt <name.txt> -o <name.txt> #split by tab or |")
    parser.add_argument('-o', type=str, default='output.txt', help="output file")
    parser.add_argument('--ct', type=str, default='x', help="ct")
    parser.add_argument('--name', type=str, default='\\textit{\\color{white}   aaaaaaaaaaa}', help="name (b or B for blank)")
    parser.add_argument('--time', type=str, default='\\textit{\\color{white}   aaaaaaaaaaa}', help="time")
    parser.add_argument('--loc', type=str, default='\\textit{\\color{white}   aaaaaaaaaaa}', help="location")

    args = parser.parse_args()

    if len(args.tsv) > 0:
        printTSV(args.tsv, args.o)
    if len(args.txt) > 0:
        printList(None, args.txt, args.o)
    if len(args.name) > 0:
        printN(args.ct, args.name, args.time, args.loc, args.o)