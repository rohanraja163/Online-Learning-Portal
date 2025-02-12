#online learning portal
#for admin page
#   username: admin
#   password: 123
from tkinter import *
from tkinter import messagebox as msg
from tkinter import ttk
import mysql.connector as sql
import webbrowser as wb
import random as rand
from PIL import ImageTk, Image
con = sql.connect(host='127.0.0.1',user='root',password='root1234',charset='utf8')
cur = con.cursor()
cur.execute('create database if not exists onlineportal')
cur.execute('use onlineportal')
cur.execute('create table if not exists users(username varchar(20), password varchar(30))')
BG = '#F9C662'
def login_page():
    def new_acc():
        def create():
            cur.execute('select * from users')
            data = cur.fetchall()
            users = [i[0] for i in data]
            un,pw = e1.get(),e2.get()
            try:
                assert (un not in users) and '' not in (un,pw) and un != 'admin' and len(un) < 15
                cur.execute(f'insert into users values("{un}","{pw}")')
                con.commit()
                n_acc.withdraw()
                login.deiconify()
                msg.showinfo('SUCCESS!','Account created!')
            except:
                msg.showwarning('ERROR','USERNAME OR PASSWORD IS INVALID OR TAKEN')
        def back():
            n_acc.withdraw()
            login.deiconify()
        login.withdraw()
        n_acc = Tk()
        n_acc.title('Create an account')
        n_acc.geometry('502x300')
        n_acc.configure(bg=BG)
        Label(n_acc,text='Create a new account',font=('comic sans ms',30),fg='yellow',bg='black',width=30).pack(side=TOP)
        Label(n_acc,text='Username',font=('comic sans ms',18),fg='yellow',bg='black',width=9).place(x=70,y=87)
        e1 = Entry(n_acc)
        e1.place(x=180,y=90)
        Label(n_acc,text='Password',font=('comic sans ms',18),fg='yellow',bg='black',width=9).place(x=70,y=147)
        e2 = Entry(n_acc)
        e2.place(x=180,y=150)
        Button(n_acc,text='Create',command=create,width=12,font=('comic sans ms',18)).place(x=175,y=210,height=50)
        Button(n_acc,text='Back',command=back,width=8,font=('comic sans ms',17),fg='red').place(x=410,y=250,height=50)
    def sign_in():
        def signin():
            cur.execute('select * from users')
            data = cur.fetchall()
            un,pw = e1.get(),e2.get()
            if (un,pw) != ('admin','123'):
                try:
                    assert ((un,pw) in data)
                    portalcall(un)
                    s_in.withdraw()
                except AssertionError:
                    msg.showwarning('ERROR','USERNAME OR PASSWORD IS INVALID')
            else:
                s_in.withdraw()
                admin = Tk()
                admin.title('Admin')
                admin.configure(bg=BG)
                admin.geometry('450x300')
                def view():
                    def back1():
                        view.withdraw()
                        admin.deiconify()
                    admin.withdraw()
                    view = Tk()
                    view.configure(bg=BG)
                    view.title('Viewer')
                    view.geometry('500x500')
                    scrollbar = Scrollbar(view, orient='vertical')
                    scrollbar.pack(side=RIGHT,fill='y')
                    text = Text(view,width=48,height=30,yscrollcommand=scrollbar.set)
                    scrollbar.config(command=text.yview)
                    text.pack()                   
                    Button(view,text='Back',command=back1,width=8,font=('comic sans ms',17),fg='red').place(x=393,y=450,height=50)
                    cur.execute('select * from progress')
                    data = cur.fetchall()
                    text.insert(END,'-'*48)
                    text.insert(END,'||     User     ||Math||Phy ||Chem|| CS ||Eng ||')
                    text.insert(END,'-'*48)
                    for i in data:
                        for j in i:
                            if type(j) == str:
                                pos = 14
                                x = '||'+str(j)+' '*(pos-len(str(j)))
                            else:
                                pos = 4
                                j*=10
                                x = '||'+str(j)+'%'+' '*(pos-len(str(j))-1)
                            text.insert(END,x)
                        text.insert(END,'||')
                        text.insert(END,'-'*48)
                    text.config(state= DISABLED)
                def deleterec():
                    def back1():
                        delete.withdraw()
                        admin.deiconify()
                    def purge():
                        delun = e1.get()
                        cur.execute('select * from users')
                        data = cur.fetchall()
                        users = [i[0] for i in data]
                        if delun in users:
                            cur.execute(f'delete from progress where user = "{delun}"')
                            con.commit()
                            cur.execute(f'delete from users where username = "{delun}"')
                            con.commit()
                            e1.delete(0, 'end')
                            msg.showinfo('Deleted','User has been deleted from server')
                        else:
                            e1.delete(0, 'end')
                            msg.showwarning('ERROR','USERNAME DOES NOT EXIST')
                    admin.withdraw()
                    delete = Tk()
                    delete.configure(bg=BG)
                    delete.title('Delete record')
                    delete.geometry('400x300')
                    Label(delete,text='Delete record',font=('comic sans ms',26),fg='red',bg='black',width = 100).pack()
                    Label(delete,text='Enter username to delete:',font=('comic sans ms',18),fg='orange',bg='black').place(x=85,y=90)
                    e1 = Entry(delete)
                    e1.place(x=103,y=135)
                    Button(delete,text='Delete',command=purge,width=8,font=('comic sans ms',15),fg='red').place(x=163,y=170)
                    Button(delete,text='Back',command=back1,width=8,font=('comic sans ms',17),fg='red').place(x=308,y=250,height=50)
                def backout():
                    login.deiconify()
                    admin.withdraw()
                Label(admin,text='Admin Page',font=('comic sans ms',26),fg='cyan',bg='black',width = 100).pack()
                Button(admin,text='View records',command=view,font=('comic sans ms',18),width=15).place(x=135,y=80,height=50)
                Button(admin,text='Delete user',command=deleterec,font=('comic sans ms',18),width=15).place(x=135,y=150,height=50)
                Button(admin,text='Logout',command=backout,width=8,font=('comic sans ms',17),fg='red').place(x=358,y=250,height=50)
        def back():
            s_in.withdraw()
            login.deiconify()
        login.withdraw()
        s_in = Tk()
        s_in.title('Sign in')
        s_in.geometry('502x300')
        s_in.configure(bg=BG)
        Label(s_in,text='Sign in',font=('comic sans ms',30),fg='cyan',bg='black',width=30).pack(side=TOP)
        Label(s_in,text='Username',font=('comic sans ms',18),fg='cyan',bg='black',width=9).place(x=70,y=87)
        e1 = Entry(s_in)
        e1.place(x=180,y=90)
        Label(s_in,text='Password',font=('comic sans ms',18),fg='cyan',bg='black',width=9).place(x=70,y=147)
        e2 = Entry(s_in)
        e2.place(x=180,y=150)
        Button(s_in,text='Sign in',command=signin,width=12,font=('comic sans ms',18)).place(x=175,y=210,height=50)
        Button(s_in,text='Back',command=back,width=8,font=('comic sans ms',17),fg='red').place(x=410,y=250,height=50)
    login = Tk()
    login.title('Login')
    login.geometry('502x300')
    path = "fp.png"
    img = ImageTk.PhotoImage(Image.open(path))
    panel = Label(login, image=img)
    panel.photo = img
    panel.place(x=-4,y=0)
    Label(login,text='Welcome to XYZ Edu Portal',font=('comic sans ms',38),fg='white',bg='black').pack(side=TOP)
    Button(login,text='New account',command=new_acc,font=('comic sans ms',20),width=15).place(x=150,y=110,height=50)
    Button(login,text='Sign In',command=sign_in,font=('comic sans ms',20),width=15).place(x=150,y=190,height=50)  
    def portalcall(un):
        def logout():
            portal.withdraw()
            login.deiconify()
        def progressbar(ind,X,Y):
            for _ in range(data[ind]):
                Label(portal,text='',font=('comic sans ms',10),bg='#66ff00',width=3).place(x=X,y=Y,height=40)
                X+=35
        def getsubject(sub):
            def back():
                vidwin.withdraw()
                portal.deiconify()
            def geturl(url):
                wb.open_new_tab(url)
            def start(sub):
                vidwin.withdraw()
                portal.withdraw()
                listofqns = [i for i in range(len(quizqns[sub]))]
                qlist = rand.sample(listofqns,len(listofqns))
                qn,corr = qlist.pop(),0
                qcount = 0
                quiz = Toplevel()
                label = Label(quiz,text='',font=('comic sans ms',20),fg='white',bg='black',width=500)
                label.pack()
                var = StringVar()
                def initqns():
                    def answer():
                        nonlocal qn,corr,qcount
                        ch = var.get()
                        if ch == str(quizqns[sub][qn][5]): corr += 1
                        try:
                            qn = qlist.pop()
                        except:
                            pass
                        qcount += 1
                        initqns()
                    quiz.title('Quiz')
                    quiz.configure(bg=BG)
                    quiz.geometry('600x400')
                    if qcount < 5:
                        label.configure(text=quizqns[sub][qn][0])
                        r1 = Radiobutton(quiz,text= quizqns[sub][qn][1].capitalize(),variable=var,value='1',width=42)
                        r1.place(x=100,y=100)
                        r2 = Radiobutton(quiz,text= quizqns[sub][qn][2].capitalize(),variable=var,value='2',width=42)
                        r2.place(x=100,y=150)
                        r3 = Radiobutton(quiz,text= quizqns[sub][qn][3].capitalize(),variable=var,value='3',width=42)
                        r3.place(x=100,y=200)
                        r4 = Radiobutton(quiz,text= quizqns[sub][qn][4].capitalize(),variable=var,value='4',width=42)
                        r4.place(x=100,y=250)
                        if qcount == 0: Button(quiz,text='Submit',width=8,font=('comic sans ms',25),fg='blue',command=answer).pack(side=BOTTOM)
                    else:
                        def home():
                            result.withdraw()
                            portalcall(un)
                        quiz.withdraw()
                        result = Tk()
                        result.title('Result')
                        result.configure(bg=BG)
                        result.geometry('300x280')
                        cur.execute(f'update progress set {sub}={corr*2} where user = "{un}"')
                        con.commit()
                        Label(result,text='Results',font=('comic sans ms',22),fg='cyan',bg='black',width = 100).pack()
                        Label(result,text=f'Correct: {corr}',font=('comic sans ms',17),fg='green',bg='black',width = 20).place(x=40,y=50)
                        Label(result,text=f'Incorrect: {qcount-corr}',font=('comic sans ms',17),fg='red',bg='black',width = 20).place(x=40,y=90)
                        Button(result,text='Home',width=8,font=('comic sans ms',25),fg='blue',command=home).pack(side=BOTTOM)
                initqns()
            sublinks = {
                'math':('https://www.youtube.com/watch?v=TMubSggUOVE','Math'),'phy':('https://www.youtube.com/watch?v=b1t41Q3xRM8','Physics'),
                'chem':('https://www.youtube.com/watch?v=-KfG8kH-r3Y','Chemistry'),'cs':('https://www.youtube.com/watch?v=_xQNeOTRyig','Computer Science'),
                'eng':('https://www.youtube.com/watch?v=XjT29tOmXlc','English')
                }
            portal.withdraw()
            vidwin = Toplevel()
            vidwin.title(sublinks[sub][1])
            vidwin.geometry('502x300')
            path2 = sub+".png"
            img2 = ImageTk.PhotoImage(Image.open(path2))
            panel2 = Label(vidwin, image=img2)
            panel2.photo = img2
            panel2.place(x=-4,y=0)
            Label(vidwin,text=sublinks[sub][1],font=('comic sans ms',30),fg='white',bg='black',width=500).pack()
            Label(vidwin,text='Watch the video and finish the quiz',font=('comic sans ms',20),fg='#66ff00',bg='black',width=30).place(x=60,y=80)
            link = Label(vidwin,text=sublinks[sub][0],font=('comic sans ms',14),width=40)
            link.place(x=75,y=120)
            link.bind("<Button-1>", lambda e: geturl(sublinks[sub][0]))
            Button(vidwin,text='Back',command=back,width=8,font=('comic sans ms',17),fg='red').place(x=410,y=250,height=50)
            Button(vidwin,text='Start quiz',command=lambda: start(sub),width=10,font=('comic sans ms',25),fg='green').place(x=170,y=160)
        portal = Tk()
        portal.title('Portal')
        portal.configure(bg=BG)
        portal.geometry('800x600')
        cur.execute('create table if not exists progress(user varchar(20), math int(3), phy int(3), chem int(3), cs int(3), eng int(3))')
        cur.execute(f'select * from progress where user = "{un}"')
        data = cur.fetchall()
        if len(data)!=0: data = list(data[0])
        if un not in data:
            cur.execute(f'insert into progress values("{un}",0,0,0,0,0)')
            con.commit()
        Label(portal,text='',font=('comic sans ms',4),bg='green',width=1000).pack(side=TOP)
        Label(portal,text=f'{un}\'s EduPortal',font=('comic sans ms',38),fg='white',bg='black',width=100).pack(side=TOP)
        Label(portal,text='',font=('comic sans ms',4),bg='green',width=1000).pack(side=TOP)
        cur.execute(f'select * from progress where user="{un}"')
        data = cur.fetchall()[0]
        Label(portal,text='PROGRESS',font=('comic sans ms',15),fg='white',bg='black',width=30).place(x=320,y=110)
        #math
        Button(portal,text='Math',command=lambda: getsubject('math'),font=('comic sans ms',20),width=15,fg='red').place(x=70,y=150,height=50)
        Label(portal,text='',font=('comic sans ms',10),bg='grey',width=50).place(x=280,y=150,height=50)
        progressbar(1,285,155)
        #phy
        Button(portal,text='Physics',command=lambda: getsubject('phy'),font=('comic sans ms',20),width=15,fg='orange').place(x=70,y=230,height=50)
        Label(portal,text='',font=('comic sans ms',10),bg='grey',width=50).place(x=280,y=230,height=50)
        progressbar(2,285,235)
        #chem
        Button(portal,text='Chemistry',command=lambda: getsubject('chem'),font=('comic sans ms',20),width=15,fg='purple').place(x=70,y=310,height=50)
        Label(portal,text='',font=('comic sans ms',10),bg='grey',width=50).place(x=280,y=310,height=50)
        progressbar(3,285,315)
        #cs
        Button(portal,text='Computer Science',command=lambda: getsubject('cs'),font=('comic sans ms',20),width=15,fg='green').place(x=70,y=390,height=50)
        Label(portal,text='',font=('comic sans ms',10),bg='grey',width=50).place(x=280,y=390,height=50)
        progressbar(4,285,395)
        #eng
        Button(portal,text='English',command=lambda: getsubject('eng'),font=('comic sans ms',20),width=15,fg='blue').place(x=70,y=470,height=50)
        Label(portal,text='',font=('comic sans ms',10),bg='grey',width=50).place(x=280,y=470,height=50)
        progressbar(5,285,475)
        Button(portal,text='Logout',command=logout,width=8,font=('comic sans ms',17),fg='red').place(x=708,y=550,height=50)
quizqns = {'eng':
               [('What is a synonym for "large"?','whale','pig','enormous','earth shaker',3),
                ('Correct contraction for "they are"','thre','they\'re','they are','their',2),
                ('Plural of "mouse"','mice','mouses','mices','pests',1),
                ('Who was the main character of "Sherlock Holmes"?','Your mother','Sherlock','Anakin Skywalker','James Bond',2),
                ('"His ____ behavior during the test led to his expulsion."','pompous','tenacious','voracious','surreptitious',4),
                ('What is the term for a word that has the opposite meaning of another word?', 'Antonym', 'Synonym', 'Homonym', 'Palindrome', 1),
                ('Which literary device is used to compare using "like" or "as"?', 'Simile', 'Metaphor', 'Alliteration', 'Onomatopoeia', 1),
                ('What is a word that sounds like the noise it represents?', 'Onomatopoeia', 'Palindrome', 'Hyperbole', 'Irony', 1),
                ('Which part of speech is used to describe a verb', 'Adverb', 'Noun', 'Pronoun', 'Conjunction', 1)],
           'cs':
               [('How do you terminate a python loop?','fracture','continue','pass','break',4),
                ('___ cannot exist without except statement','fry','try','cry','attempt',2),
                ('Output: "100+100" ','200','100100','100+100','Error',3),
                ('Python is a ____ level language','high','advanced','low','top',1),
                ('while True runs ___','for 1 iteration','if the cause is true and the fight is against injustice','until "break" is given','loop does not run',3),
                ('Which of the following is not a valid Python variable name?', '123var', 'my_var', '_var', 'Var123', 1),
                ('What data type is used to store a sequence of characters in Python?', 'String', 'List', 'Integer', 'Float', 1),
                ('Which keyword is used to define a function in Python?', 'def', 'function', 'define', 'func', 1)],
           'chem':
               [('HCl+NaOH-->','HClNaOH','No reaction','benzene','NaCl+Water',4),('Valency of carbon is __','2','1','4','3',3),
                ('What is the chemical symbol for potassium?', 'K', 'P', 'Pt', 'Kr', 1),
                ('Benzene has __','3 double bond','1 triple bond','bonds of friendship','2 double bond',1),
                ('Reactions absorbing heat are __thermic','heat','photo','exo','endo',4),
                ('Organic chemistry is __','annoying','the study of carbon compunds','making bombs','study of periodic table',2),
                ('What is the chemical symbol for silver?', 'Ag', 'Au', 'Si', 'Sr', 1),
                ('Which gas is known as laughing gas?', 'Nitrous oxide', 'Carbon monoxide', 'Oxygen', 'Methane', 1),
                ('What is the chemical symbol for gold?', 'Au', 'Ag', 'Fe', 'Cu', 1),
                ('What is the chemical formula for water?', 'H2O', 'CO2', 'O2', 'NaCl', 1),
                ('Which element is essential for life and makes up most of the Earth’s atmosphere?', 'Oxygen', 'Nitrogen', 'Carbon', 'Hydrogen', 2),
                ('What is the chemical formula for methane?', 'CH4', 'CO2', 'H2O', 'C6H12O6', 1)],
           'phy':
               [('v = ','v-v','u+at','u-at','u+2a',2),('SI unit of resistance','ohm','newton','pascal','tesla',1),
                ('s = ut + __ at^2','1/2','2','1','3/2',1),
                ('Bending of light is called __','light bending','reflection','refraction','curving',3),
                ('What is the SI unit of energy?', 'Joule (J)', 'Newton (N)', 'Watt (W)', 'Volt (V)', 1),
                ('What is the speed of light in a vacuum?', '299,792,458 meters per second', '100,000 meters per second', '3,000,000 meters per second', '186,282 miles per hour', 1),
                ('Light shows both __ nature','types of','wave and particle','illuminating and heating','blinding and shocking',2),
                ('What is the formula for calculating kinetic energy?', 'KE = 0.5 * m * v^2', 'KE = m * g * h', 'KE = F * d', 'KE = P * t', 1),
                ('What is the SI unit of energy?', 'Joule (J)', 'Newton (N)', 'Watt (W)', 'Volt (V)', 1),
                ('What is the SI unit of electric charge?', 'Coulomb (C)', 'Volt (V)', 'Ampere (A)', 'Ohm (Ω)', 1)],
           'math':
               [(' d(e^x)/dx','e^x','1','xe','xe^(x-1)',1),
                ('(A+B)^2','A+B+A+B','A+2AB+B','A^2+2AB+B^2','A^2-B^2',3),
                ('3-10/10+1','3/10','-7/11','2','Not defined',3),
                ('log(a)+log(b) = ','log(a/b)','log(ab)','2log(ab)','(ab)log(1)',2),
                ('Modulus any number cannot be','0','negative','positive','a number',2),
                ('What is the square root of 144?', '12', '6', '16', '10', 1),
                ('In a right triangle, which side is opposite to the right angle?', 'Hypotenuse', 'Adjacent', 'Opposite', 'Base', 1),
                ('What is the result of 3 squared?', '9', '6', '12', '15', 1),
                ('What is the value of π (pi) to two decimal places?', '3.14', '3.41', '3.21', '3.05', 1),
                ('What is the term for a polygon with eight sides?', 'Octagon', 'Hexagon', 'Decagon', 'Nonagon', 1),
                ('What is the term for the longest side of a right triangle?', 'Hypotenuse', 'Adjacent', 'Opposite', 'Base', 1)]        
               }
login_page()
