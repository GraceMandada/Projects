import Crawler_FileTraverser

from tkinter import *
from tkinter import ttk

def func():
	search_term=text2b.get()
	final_search=search_term
	out_search_term=''
	rq=0
	n=0
	n_2=0
	bq=0
	if '?q' in search_term:
		if "%20" in search_term:
			if '&' in search_term:
				p=search_term[search_term.index('=')+1:search_term.index('&')]
				q=p.split('%20')
				final_search=''
				for g in q:
					final_search+=g
				bq=1
			else:
				p=search_term[search_term.index('=')+1::]
				q=p.split('%20')
				final_search=''
				for g in q:
					final_search+=g
				bq=1
		if 'num_results=' in search_term:
			h=search_term.split('num_results=')
			print(h)
			if '&' in h[1]:
				h=h[1][:h[1].index('&')]
			try:
				n=int(h[1])
				rq=1
			except:
				n=int(h)
				rq=1
		if 'offset=' in search_term:
			h=search_term.split('offset=')
			print(h)
			if '&' in h[1]:
				h=h[1][:h[1].index('&')]
			try:
				n_2=int(h)
				rq=1
			except:
				n_2=int(h[1])
				rq=1
		if rq==0 and bq==0:
			e=search_term.split('=')
			final_search=e[1]
	search_term=final_search
	a=Crawler_FileTraverser.search(search_term)
	b=a.split(',')
	start=a.index('[')
	end=a.index(']')
	out=a[start+1:end]
	f_list=out.split(',')
	if rq==1:
		if n==0:
			n=len(f_list)
	time_taken=b[-2]
	total_res=str(len(f_list))
	s='     '+time_taken+' '+'total results : '+total_res+'\n'
	if rq==1:
		f_list=f_list[n_2:n]
	for x in f_list:
		temp_str=''
		re=list(search_term)
		q=list(x)
		se=x.index(search_term)
		print(re)
		p=0
		for y in range(0,len(q)):
			if y==se:
				p=1
			if p==1:
				for t in range(0,len(re)):
					temp_str+=re[t].upper()
				p=0
			else:
				if y not in range(se,se+len(re)):
					temp_str+=q[y]
		f_list[f_list.index(x)]=temp_str

	for j in f_list:
		s+=j+'\n'
	l.config(text=s)

def bookmark():
	a=open('BookMarks_db.txt','a')
	temp_l=text5b.get('1.0', 'end-1c')
	c=temp_l.split('\n')
	for g in c:
		a.write(g)
		a.write('\n')
	a.close()

master = Tk()                                           
master.geometry("1600x1400")
master.config(background='white')
master.title("Search Engine")
heading = Label(master, text="Web Search Engine GUI", font=("Free Ink",20,"bold"), bg="purple", width=90, relief="solid", bd=2, fg='white')
subheading2  = Label(master, text="Search", font="Arial 35 bold", bg="white")
subheading4  = Label(master, text="Results", font="Arial 25 bold", bg="white")
subheading5  = Label(master, text="BookMarks", font="Arial 25 bold", bg="white")
text2b     = Entry(master, width=80, bg= "light blue", relief="solid", bd=2)
"""text4b     = Text(master, width=80, height=40, bg='light grey')
text4b.pack()"""
text5b     = Text(master, width=50, height=10, bg='light grey')
text5b.pack()
l = Label(master,text='None',bg='white')
button2    = Button(master, command=func, height=2, width=15, text="Search", relief="solid", bd=2, bg="orange")
button3    = Button(master, command=bookmark, height=2, width=15, text="Add", relief="solid", bd=2, bg="orange")
heading       .pack(side=TOP, fill=X)
subheading2   .place(x=90, y=60)
subheading4   .place(x=1030, y=60)
subheading5   .place(x=80, y=350)
text2b        .place(x=90, y=150)
#text4b        .place(x=700, y=120)
text5b        .place(x=80, y=400)
button2       .place(x=240, y=220)
button3       .place(x=240, y=640)
l.pack()
l.place(x=650,y=130)
master.mainloop()