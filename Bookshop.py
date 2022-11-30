import mysql.connector
import pyfiglet
import sys
from tabulate import tabulate
import os

co = mysql.connector.connect(host='localhost',user='root',password='123456')
cu = co.cursor(buffered=True)

def create():
    cu.execute('show databases')
    x = cu.fetchall()
    if ('bookshop',) not in x:
        cu.execute('create database Bookshop')
    cu.execute('use bookshop')
    cu.execute('show tables')
    y = cu.fetchall()
    if ('stocks',) not in y:
        cu.execute('create table stocks (SlNo int primary key not null, Name varchar(40) not null, Author varchar(30) not null, Pub varchar(30), Qty int, Price float)')

def gui():
    os.system('cls')
    print(pyfiglet.figlet_format('BookShop','doom')+'====================================\n')
    print("1) Add a Book\n2) Display Books\n3) Change Book Details\n4) Delete a Book\n\n+---------------------------------+\n| '-Menu-' -> Back to Main Menu   |\n| '-Close-' -> Exit the Program   |\n| '-Cts-' -> Custom MYSQL Command |\n+---------------------------------+\n\n====================================")
    while True:
        x = inp('\nEnter corresponding Action Number : ','int',True)
        if x==1:
            os.system('cls')
            print('---------------------------------------------------------\n'+pyfiglet.figlet_format('Book Insertion','small')+'---------------------------------------------------------\n')
            insert()
        elif x==2:
            os.system('cls')
            print('------------------------------------------------------\n'+pyfiglet.figlet_format('Book Display','small')+'------------------------------------------------------')
            print("\n1) All Stocks\n2) Specific Criteria of Stocks\n")
            y = inp(': ','1o2')
            display(y)
        elif x==3:
            os.system('cls')
            print('------------------------------------------------------\n'+pyfiglet.figlet_format('Book Updation','small')+'------------------------------------------------------')
            print("\n1) Single Updation\n2) Group Updation\n")
            y = inp(': ','1o2')
            update(y)
        elif x==4:
            os.system('cls')
            print('------------------------------------------------------\n'+pyfiglet.figlet_format('Book Removal','small')+'------------------------------------------------------')
            print("\n1) Single Removal\n2) Group Removal\n")
            y = inp(': ','1o2')
            remove(y)
        else:
            print('Error! Invalid Input. Try Again.\n')
            continue

def insert():
    while True:
        a = slnodupe()
        b = inp('Enter Book Title : ','str',True,True)
        c = inp('Enter Author : ','char',True,True)
        d = inp('Enter Publisher Name : ','str',False,True)
        e = inp('Enter Quantity : ','int',False,True)
        f = inp('Enter Price : ','float',False,True)
        print('\nPreview\n-------')
        print('|',a,'|',b,'|',c,'|',d,'|',e,'|',f,'|')
        x = inp('\nConfirm Addition : ','yn')
        if x==True:
            try:
                dml('Insert into stocks values (%s,%s,%s,%s,%s,%s)'%(a,b,c,d,e,f))
                gui()
            except mysql.connector.errors.IntegrityError:
                print('Error! Duplicate SlNo. Try Again.\n')
                continue
        else:
            print('\n')
            continue

def display(x):
    if x==False:
        print('\n'+str(pyfiglet.figlet_format('All Stocks','small')),end='')
        table('Select * from stocks')
        y = inp('\nPress ENTER to continue... ','str')
        gui()
    else:
        print('\n'+str(pyfiglet.figlet_format('Specific Stocks','small')))
        while True:
            a = inp('Enter Column Names (Select [Columns]) : ','str',True)
            b = inp('Enter Conditions (from stocks [Conditions]) : ','str')
            print()
            try:
                table('Select %s from stocks %s'%(a,b))
                y = inp('\nPress ENTER to continue... ','str')
                gui()
            except mysql.connector.errors.ProgrammingError:
                print('Error! Incorrect Column Name or Syntax. Try Again.\n')
                continue

def update(x):
    if x==False:
        print('\n'+str(pyfiglet.figlet_format('Single Updation','small')))
        while True:
            y = slnomatch()
            print()
            table('Select * from stocks where SlNo=%s'%(y,))
            print()
            z = columnmatch()
            a = inp('Enter New Value : ','str',False,z)
            print()
            b = inp('Confirm Updation : ','yn')
            if b==True:
                try:
                    dml('Update stocks set %s = %s where SlNo=%s'%(z,a,y))
                    gui()
                except mysql.connector.errors.ProgrammingError:
                    print('Error! Incorrect Column Name or Syntax. Try Again.\n\n')
                    continue 
            else:
                print()
                update(x)
    else:
        print('\n'+str(pyfiglet.figlet_format('Group Updation','small')))
        while True:
            table('Select * from stocks')
            print()
            z = columnmatch('slno')
            a = inp('Enter New Value : ','str',False,True)
            b = inp('Enter Conditions (from stocks [Conditions]) : ','str')
            f = inp('\nConfirm Updation : ','yn')
            if f==True:
                try:
                    dml('Update stocks set %s = %s %s'%(z,a,b))
                    gui()
                except mysql.connector.errors.ProgrammingError:
                    print('Error! Incorrect Column Name or Syntax. Try Again.\n')
                    continue
            else:
                print()
                update(x)

def remove(x):
    if x==False:
        print('\n'+str(pyfiglet.figlet_format('Single Removal','small')))
        while True:
            y = slnomatch()
            print()
            table('Select * from stocks where SlNo=%s'%(y,))
            a = inp('\nConfirm Removal : ','yn')
            if a==True:
                try:
                    dml('Delete from stocks where SlNo=%s'%(y,))
                    gui()
                except mysql.connector.errors.ProgrammingError:
                    print('Error! Incorrect Column Name or Syntax. Try Again.\n')
                    continue 
            else:
                print()
                remove(x)
    else:
        print('\n'+str(pyfiglet.figlet_format('Group Removal','small')))
        while True:
            table('Select * from stocks')
            a = inp('\nEnter Conditions (from stocks [Conditions]) [to delete all records leave as blank] : ','str')
            b = inp('\nConfirm Updation : ','yn')
            if b==True:
                try:
                    dml('Delete from stocks %s'%(a,))
                    print()
                    table('Select * from stocks')
                    y = inp('\nPress ENTER to continue... ','str')
                    gui()
                except mysql.connector.errors.ProgrammingError:
                    print('Error! Incorrect Column Name or Syntax. Try Again.\n')
                    continue 
            else:
                print()
                remove(x)

def dml(x):
    global cu
    cu.execute(x)
    co.commit()
    try:
        y = cu.fetchall()
        return y
    except TypeError:
        pass

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def inp(x,y,z=False,w=False):
    while True:
        if w=='slno':
            a = slnodupe()
            return str(a)
        a = input(x)
        if a.lower()=='-menu-':
            gui()
        elif a.lower()=='-close-':
            sys.exit()
        elif a.lower()=='-cts-':
            try:
                b = inp('\nEnter Custom Command (use " instead of \' ) : ','str')
                c = dml(b)
                if c!=None:
                    print()
                    table(None,c)
                    d = inp('\nPress ENTER to continue... ','str')
                    gui()
            except mysql.connector.errors.ProgrammingError:
                print('Error! Try Again.')
                gui()
        elif z==True and a=='':
            print('Error! Value cant be blank. Try Again.\n')
            continue
        elif (w=='name' or w=='pub') and a.isdigit()==False:
            return '"'+str(a)+'"'
        elif w=='author' and any(chr.isdigit() for chr in a)!=True:
            return '"'+str(a)+'"'
        elif (w=='qty' or w=='price') and a.isdigit():
            if w=='price':
                return float(a)
            else:
                return int(a)
        elif a.lower().startswith(('qty','price')) and (s in a for s in ('+','-','*','/')) and w!=False:
            return str(a)
        elif a.lower().startswith(('slno','name','author','pub')) and (s in a for s in ['+','-','*','/']) and w!=False:
            print('Error! Invalid Input. Try Again1.\n')
            continue
        elif w==True:
            if a=='':
                return 'NULL'
            elif isfloat(a) and y=='float':
                return float(a)
            elif a.isdigit() and y=='int':
                return int(a)
            elif (a.isdigit()==False and (y=='int' or y=='float')) or (a.isdigit()==True and y=='str') or (any(chr.isdigit() for chr in a) and y=='char'):
                print('Error! Invalid Input. Try Again.\n')
                continue
            else:
                return '"'+str(a)+'"'
        elif y=='yn':
            if a.lower()=='y':
                return True
            elif a.lower()=='n':
                return False
            else:
                print('Error! Invalid Input. Try Again.')
                continue
        elif (a=='1' or a=='2') and y=='1o2':
            if a=='1':
                return False
            else:
                return True
        elif a.isnumeric() and y=='int':
            return int(a)
        elif isfloat(a) and y=='float':
            return float(a)
        elif a.isascii() and y=='str':
            return str(a)
        elif z==False and a=='':
            return str(a)
        else:
            print('Error! Invalid Input. Try Again.\n')

def table(x,y=[]):
    global cu
    if x!=None:
        cu.execute(x)
        a = cu.fetchall()
    else:
        a = y
    column = []
    values = []
    c = 0
    for i in cu.description:
        column.append(i[0])
    for i in a:
        values.append([])
        for j in i:
            if j==None:
                values[c].append('NULL')
            else:
                values[c].append(j)
        c += 1
    print(str(tabulate(values, headers=column, tablefmt='psql')))

def slnomatch():
    global cu
    cu.execute('Select SlNo from stocks')
    sl = cu.fetchall()
    isBreak = False
    while isBreak==False:
        y = inp('Enter SlNo of Book : ','str')
        for i in sl:
            if y==str(i[0]):
                isBreak = True
        if isBreak==False:
            print('Error! Unknown SlNo. Try Again.\n')
    return y

def slnodupe():
    global cu
    cu.execute('Select SlNo from stocks')
    sl = cu.fetchall()
    while True:
        isBreak = True
        a = inp('Enter Serial No. : ','int')
        for i in sl:
            if a==i[0]:
                isBreak = False
        if a=='':
            isBreak = False
        if isBreak==True:
            break
        else:
            print('Error! Invalid SlNo. Try Again.\n')
    return a

def columnmatch(*x):
    global cu
    c,d = 0,-1
    cu.execute('Select * from stocks')
    while True:
        z = inp('Enter Column Name : ','str')
        for i in cu.description:
            if i[0].lower()==z.lower():
                d = c
            c += 1
        if d==-1 or any(z.lower()==i for i in x):
            print('Error! Unknown Column Name. Try Again.\n')
            continue
        break
    return z.lower()

create()
gui()
