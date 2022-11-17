import mysql.connector
import pyfiglet
import sys
from tabulate import tabulate
# Temp imports
import os
import subprocess

paswd = input('Enter MySQL password : ')

co = mysql.connector.connect(host='localhost',user='root',password=paswd)
cu = co.cursor()

def create():
    cu.execute('show databases')
    x = cu.fetchall()
    if ('bookshop',) not in x:
        cu.execute('create database Bookshop')
    cu.execute('use bookshop')
    cu.execute('show tables')
    y = cu.fetchall()
    if ('stocks',) not in y:
        cu.execute('create table stocks (SlNo int primary key not null, Name varchar(40) not null, Author varchar(30) not null, Pub varchar(30), Qty int, Price int)')

def gui():
    print('\n'*50)
    print(pyfiglet.figlet_format('BookShop','doom')+'====================================\n')
    print("1) Add a Book\n2) Display Books\n3) Change Book Details\n4) Delete a Book\n\n+-------------------------------+\n| '-Menu-' -> Back to Main Menu |\n| '-Close-' -> Exit the Program |\n+-------------------------------+\n\n====================================\n")
    x = inp('Enter corresponding Action Number : ','int',True)
    if x==1:
        print('\n'*50)
        print('---------------------------------------------------------\n'+pyfiglet.figlet_format('Book Insertion','small')+'---------------------------------------------------------\n')
        insert()
    elif x==2:
        print('\n'*50)
        print('------------------------------------------------------\n'+pyfiglet.figlet_format('Book Display','small')+'------------------------------------------------------')
        print("\n1) All Stocks\n2) Specific Criteria of Stocks\n")
        y = inp(': ','1o2')
        display(y)
    elif x==3:
        print('\n'*50)
        print('------------------------------------------------------\n'+pyfiglet.figlet_format('Book Updation','small')+'------------------------------------------------------')
        print("\n1) Single Updation\n2) Group Updation\n")
        y = inp(': ','1o2')
        update(y)
    elif x==4:
        print('\n'*50)
        print('------------------------------------------------------\n'+pyfiglet.figlet_format('Book Removal','small')+'------------------------------------------------------')
        print("\n1) Single Removal\n2) Group Removal\n")
        y = inp(': ','1o2')
        remove(y)

def insert():
    while True:
        cu.execute('Select SlNo from stocks')
        sl = cu.fetchall()
        while True:
            isBreak = True
            a = inp('Enter Serial No. : ','int',True)
            for i in sl:
                if a==i[0]:
                    print('Error! Duplicate SlNo. Try Again.\n')
                    isBreak = False
            if isBreak==True:
                break
        b = inp('Enter Book Title : ','str',True)
        c = inp('Enter Author : ','str',True)
        d = inp('Enter Publisher Name : ','str',False,True)
        e = inp('Enter Quantity : ','int',False,True)
        f = inp('Enter Price : ','float',False,True)
        print('\nPreview\n-------')
        print(a,'|',b,'|',c,'|',d,'|',e,'|',f)
        x = inp('\nConfirm Addition : ','yn')
        l = [a,b,c,d,e,f]
        for i in range(len(l)):
            if str(l[i]).isdigit()==False and str(l[i])!='NULL':
                l[i] = '"'+str(l[i])+'"'
        if x==True:
            try:
                cu.execute('Insert into stocks values ('+str(l[0])+','+str(l[1])+','+str(l[2])+','+str(l[3])+','+str(l[4])+','+str(l[5])+')')
                co.commit()
                gui()
            except mysql.connector.errors.IntegrityError:
                print('Error! Duplicate Slno. Try Again.\n\n')
                continue
        else:
            print('\n')
            continue

def display(x):
    if x==False:
        print('\n'+str(pyfiglet.figlet_format('All Stocks','small')),end='')
        cu.execute('Select * from stocks')
        out = cu.fetchall()
        table(out)
        y = inp('\nContinue : ','str')
        gui()
    else:
        print('\n'+str(pyfiglet.figlet_format('Specific Stocks','small')))
        while True:
            a = inp('Enter Column Names (Select [Columns]) : ','str',True)
            b = inp('Enter Conditions (from stocks [Conditions]) : ','str')
            print()
            try:
                cu.execute('Select '+a+' from stocks '+b)
                out = cu.fetchall()
                table(out)
                y = inp('\nContinue : ','str')
                gui()
            except mysql.connector.errors.ProgrammingError:
                print('Error! Incorrect Column Name or Syntax. Try Again.\n')
                continue

def update(x):
    if x==False:
        print('\n'+str(pyfiglet.figlet_format('Single Updation','small')))
        while True:
            cu.execute('Select SlNo from stocks')
            sl = cu.fetchall()
            isBreak = False
            while isBreak==False:
                y = inp('Enter SlNo of Book : ','int',True)
                for i in sl:
                    if y==i[0]:
                        isBreak = True
                if isBreak==False:
                    print('Error! Incorrect Slno. Try Again.\n')
            cu.execute('Select * from stocks where SlNo='+str(y))
            out = cu.fetchall()
            print()
            table(out)
            print()
            c,d = 0,-1
            while True:
                z = inp('Enter Column Name : ','char',True)
                for i in cu.description:
                    if i[0].lower()==z.lower():
                        d = c
                    c += 1
                if d==-1:
                    print('Error! Incorrect Column Name. Try Again.\n')
                    continue
                break
            a = inp('Enter New Value : ','str',False,True)
            print()
            b = inp('Confirm Updation : ','yn')
            if b==True:
                try:
                    cu.execute('Update stocks set '+z+' = '+a+' where SlNo='+str(y))
                    co.commit()
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
            cu.execute('Select * from stocks')
            out = cu.fetchall()
            table(out)
            print()
            c,d = 0,-1
            while True:
                z = inp('Enter Column Name : ','char',True)
                for i in cu.description:
                    if i[0].lower()==z.lower():
                        d = c
                    c += 1
                if d==-1:
                    print('Error! Incorrect Column Name. Try Again.\n')
                    continue
                break
            a = inp('Enter Conditions (from stocks [Conditions]) : ','str')
            b = inp('Enter New Value : ','str',False,True)
            f = inp('\nConfirm Updation : ','yn')
            if f==True:
                try:
                    cu.execute('Update stocks set '+z+' = '+b+' '+a)
                    co.commit()
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
            cu.execute('Select SlNo from stocks')
            sl = cu.fetchall()
            isBreak = False
            while isBreak==False:
                y = inp('Enter SlNo of Book : ','int',True)
                for i in sl:
                    if y==i[0]:
                        isBreak = True
                if isBreak==False:
                    print('Error! Incorrect Slno. Try Again.\n')
            cu.execute('Select * from stocks where SlNo='+str(y))
            out = cu.fetchall()
            print()
            table(out)
            a = inp('\nConfirm Removal : ','yn')
            if a==True:
                try:
                    cu.execute('Delete from stocks where SlNo='+str(y))
                    co.commit()
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
            cu.execute('Select * from stocks')
            out = cu.fetchall()
            table(out)
            a = inp('\nEnter Conditions (from stocks [Conditions]) [to delete all records leave as blank] : ','str')
            b = inp('\nConfirm Updation : ','yn')
            if b==True:
                try:
                    cu.execute('Delete from stocks '+a)
                    co.commit()
                    cu.execute('Select * from stocks')
                    out = cu.fetchall()
                    print()
                    table(out)
                    y = inp('\nContinue : ','str')
                    gui()
                except mysql.connector.errors.ProgrammingError:
                    print('Error! Incorrect Column Name or Syntax. Try Again.\n')
                    continue 
            else:
                print()
                remove(x)

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def inp(x,y,z=False,w=False):
    while True:
        a = input(x)
        if a.lower()=='wew' or a.lower()=='ewe':
            subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:])
        elif a.lower()=='-menu-':
            gui()
        elif a.lower()=='-close-':
            sys.exit()
        elif a.lower()=='-test-':
            test()
        elif z==True and a=='':
            print('Error! Value cant be blank. Try Again.\n')
            continue
        elif w==True and a=='':
            return 'NULL'
        elif w==True and a!='':
            if a.isdigit():
                return str(a)
            elif a.lower().startswith(('qty','price')) and (s in a for s in ('+','-','*','/')):
                return str(a)
            elif a.lower().startswith(('slno','name','author','pub')) and (s in a for s in ('+','-','*','/')):
                print('Error! Invalid Input. Try Again.\n')
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
        elif a.isalpha() and y=='char':
            return str(a)
        elif a.isnumeric() and y=='int':
            return int(a)
        elif a.isalnum() and y=='alnum':
            return str(a)
        elif isfloat(a) and y=='float':
            return float(a)
        elif a.isascii() and y=='str':
            return str(a)
        elif z==False and a=='':
            return str(a)
        else:
            print('Error! Invalid Input. Try Again.\n')
            continue

def test():
    cu.execute('Drop table stocks')
    cu.execute('Create table stocks (SlNo int primary key not null, Name varchar(40) not null, Author varchar(30) not null, Pub varchar(30), Qty int, Price int)')
    cu.execute('Insert into stocks values (101,"Harry Potter and the Sorcerer\'s Stone","J. K. Rowling","Bloomsbury Publishing",100,299)')
    co.commit()
    cu.execute('Insert into stocks values (102,"Charlie and the Chocolate Factory","Roald Dahl","Puffin Books",50,399)')
    co.commit()
    cu.execute('Insert into stocks values (103,"Percy Jackson and the Lightning Thief","Rick Riordan","Puffin Books",75,299)')
    co.commit()
    cu.execute('Insert into stocks values (104,"A Christmas Carol","Charles Dickens","Chapman & Hall",50,99)')
    co.commit()
    cu.execute('Insert into stocks values (105,"David Copperfield","Charles Dickens","Bradbury & Evans",50,199)')
    co.commit()
    gui()

def table(x):
    column = []
    values = []
    c = 0
    for i in cu.description:
        column.append(i[0])
    for i in x:
        values.append([])
        for j in i:
            if j==None:
                values[c].append('NULL')
            else:
                values[c].append(j)
        c += 1
    print(str(tabulate(values, headers=column, tablefmt='psql')))
    return values

create()
gui()

co.close()
