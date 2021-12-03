import asyncio
from logging import root
from os import curdir
from tkinter import ttk
from tkinter import *
from cur import but
from sql import *
from cj_kw import begin_cj_kw
from cj_url import begin_cj_urls
from cj_content import begin_cj_content
import tkinter as tk
import tkinter.messagebox as messagebox


root = tk.Tk()
root.title('速卖通产品采集')
root.geometry("800x600")

w=root.winfo_screenwidth()
h=root.winfo_screenheight()

ttk.Separator(root,orient='horizontal').pack(fill=X,pady=5)

Label(root, text='关键词采集', fg="black", bg="yellow",font=("微软雅黑", 14)).pack(fill=X,padx=5)


class KwFra(Frame):
    def __init__(self,master=None):
        Frame.__init__(self, master)
        self.pack(fill=X, pady=2)
        self.alcount=IntVar(self)
        self.cjcount=IntVar(self)
        self.getCount()
        self.createWidgets()

    def createWidgets(self):
        lframe=Frame(self)
        lframe.pack(side=LEFT,pady=6,padx=6)
        f0=Frame(lframe)
        f0.grid(row=0, column=0, sticky='w') # sticky='w'指定了组件在单元格中靠左对齐
        f1=Frame(lframe)
        f1.grid(row=1, column=0, sticky='w')
        Label(f0,text='一级类目:').pack(padx=3,side=LEFT)
        Label(f0,textvariable=self.alcount).pack(padx=3,side=LEFT)
        Label(f1,text='二级类目:').pack(padx=3,side=LEFT)
        Label(f1,textvariable=self.cjcount,fg='red').pack(padx=3,side=LEFT)



        Button(self,text='刷新数据',command=self.rload_data).pack(side=LEFT,padx=20)

        Label(self, text='并发数:').pack(side=LEFT, padx=5, pady=2)
        self.typeSelect = ttk.Combobox(self,width=5,state='readonly')
        self.typeSelect['value']=[1,2,3,4,5]
        self.typeSelect.pack(side=LEFT, padx=2, pady=2)
        self.typeSelect.current(0)

        Button(self,text='开始采集',command=self.cj_kw).pack(side=LEFT,padx=20)
        Button(self,text='类目处理',command=but).pack(side=LEFT,padx=10)

    
    def getCount(self):
        res0=exe_sql('select count(cid) from class where grade=1')
        res1=exe_sql('select count(cid) from class where grade=2')
        self.alcount.set(res0[0][0])
        self.cjcount.set(res1[0][0])
    
    def cj_kw(self):
        try:
            res=asyncio.run(begin_cj_kw(w,h))
            if not res:
                messagebox.showerror('错误','采集失败请重试')

            else:
                self.getCount()
                messagebox.showinfo('提示',f'采集完成,数据库目前有{self.cjcount.get()}个二级类目')

        except Exception as e:

            print(f'cj_kw => {e}')

    def rload_data(self):
        self.getCount()
    
obkw= KwFra(master=root)

ttk.Separator(root,orient='horizontal').pack(fill=X,pady=5)
ttk.Separator(root,orient='horizontal').pack(fill=X,pady=5)

Label(root, text='网址采集', fg="black", bg="skyblue",font=("微软雅黑", 14)).pack(fill=X,padx=5)

class WzFra(Frame):
    def __init__(self,master=None):
        Frame.__init__(self, master)
        self.pack(fill=X, pady=2)
        self.alcount=IntVar(self)
        self.cjcount=IntVar(self)
        self.wzcount=IntVar(self)
        self.zdcount0=IntVar(self)
        self.zdcount1=IntVar(self)
        self.cids=-1
        self.getCount()
        self.createWidgets()

    def createWidgets(self):
        lframe=Frame(self)
        lframe.pack(side=LEFT,padx=6,pady=6)
        f0=Frame(lframe)
        f0.grid(row=0, column=0, sticky='w') # sticky='w'指定了组件在单元格中靠左对齐
        f1=Frame(lframe)
        f1.grid(row=1, column=0, sticky='w')
        f2=Frame(lframe)
        f2.grid(row=2, column=0, sticky='w')
        Label(f0,text='类目总数:').pack(padx=3,side=LEFT)
        Label(f0,textvariable=self.alcount).pack(padx=3,side=LEFT)
        Label(f1,text='类目未采集:').pack(padx=3,side=LEFT)
        Label(f1,textvariable=self.cjcount,fg='red').pack(padx=3,side=LEFT)
        Label(f2,text='当前网址总数:').pack(padx=3,side=LEFT)
        Label(f2,textvariable=self.wzcount,fg='red').pack(padx=3,side=LEFT)
        lbframe=Frame(self)
        lbframe.pack(side=LEFT,padx=6,pady=6)
        f3=Button(lbframe,text='刷新数据',command=self.rload_data)
        f3.grid(row=0, column=0, sticky='w',pady=3)
        f4=Button(lbframe,text='全部采集',command=self.cj_wz)
        f4.grid(row=1, column=0, sticky='w',pady=3)

        ttk.Separator(self,orient='vertical').pack(side=LEFT,fill=Y,padx=10)

        rframe=Frame(self)
        rframe.pack(side=LEFT,padx=6,pady=6)
        f5=Frame(rframe)
        f5.grid(row=1, column=0, sticky='w') # sticky='w'指定了组件在单元格中靠左对齐
        f6=Frame(rframe)
        f6.grid(row=2, column=0, sticky='w')
        f8=Frame(rframe)
        f8.grid(row=0, column=0, sticky='w')
        Label(f5,text='类目总数:').pack(padx=3,side=LEFT)
        Label(f5,textvariable=self.zdcount0).pack(padx=3,side=LEFT)
        Label(f6,text='类目未采集:').pack(padx=3,side=LEFT)
        Label(f6,textvariable=self.zdcount1,fg='red').pack(padx=3,side=LEFT)
        Label(f8, text='输入cid:').pack(side=LEFT, padx=3)
        self.zdinp=Entry(f8,width=10)
        self.zdinp.pack(side=LEFT,padx=3, pady=3)
        rbFrame=Frame(self)
        rbFrame.pack(side=LEFT,padx=6,pady=6)

        f9=Button(rbFrame,text='刷新数据',command=self.rload_data2)
        f9.grid(row=0, column=0, sticky='w',pady=3)
        f10=Button(rbFrame,text='指定采集',command=self.cj_wz2)
        f10.grid(row=1, column=0, sticky='w',pady=3)

        ttk.Separator(self,orient='vertical').pack(side=LEFT,fill=Y,padx=10)
        Label(self, text='并发数:').pack(side=LEFT, padx=10, pady=2)
        self.typeSelect = ttk.Combobox(self,width=5,state='readonly')
        self.typeSelect['value']=[1,2,3,4,5]
        self.typeSelect.pack(side=LEFT, padx=2, pady=2)
        self.typeSelect.current(2)


    
    def getCount(self):
        res0=exe_sql('select count(cid) from class where grade=2')
        res1=exe_sql('select count(cid) from class where grade=2 and cstate=0')
        res2=exe_sql('select count(id) from pids')
        self.alcount.set(res0[0][0])
        self.cjcount.set(res1[0][0])
        self.wzcount.set(res2[0][0])
    
    def cj_wz(self):
        try:
            self.cids=-1
            bfs=int(self.typeSelect.get())
            res=asyncio.run(begin_cj_urls(w,h,bfs,cids=self.cids))
            if not res:
                messagebox.showerror('错误','采集失败请重试')

            else:
                self.getCount()
                messagebox.showinfo('提示',f'采集完成,数据库目前有{self.wzcount.get()}个待采集网址')

        except Exception as e:

            print(f'cj_wz => {e}')
    
    def cj_wz2(self):
        try:
            if self.cids==-1:
                messagebox.showerror('错误','请先获取数据')
                return
            bfs=int(self.typeSelect.get())
            res=asyncio.run(begin_cj_urls(w,h,bfs,cids=self.cids))
            if not res:
                messagebox.showerror('错误','采集失败请重试')

            else:
                self.rload_data2()
                messagebox.showinfo('提示',f'采集完成,数据库目前有{self.wzcount.get()}个待采集网址')

        except Exception as e:

            print(f'cj_wz2 => {e}')
    
    
    def rload_data(self):
        self.getCount()
    
    def rload_data2(self):
        cids_str=self.zdinp.get()
        if not cids_str:
            messagebox.showerror('错误','请输入数据')
            return
        where=f'({cids_str})'
        self.cids=where
        res0=exe_sql(f'select count(cid) from class where cid in {where} and grade=2')
        res1=exe_sql(f'select count(cid) from class where  cid in {where} and (grade=2 and cstate=0)')
        self.zdcount0.set(res0[0][0])
        self.zdcount1.set(res1[0][0])

obwz=WzFra(master=root)

ttk.Separator(root,orient='horizontal').pack(fill=X,pady=5)
ttk.Separator(root,orient='horizontal').pack(fill=X,pady=5)

Label(root, text='内容采集', fg="black", bg="red",font=("微软雅黑", 14)).pack(fill=X,padx=5)

class CotFra(Frame):
    def __init__(self,master=None):
        Frame.__init__(self, master)
        self.pack(fill=X, pady=2)
        self.alcount=IntVar(self)
        self.cjcount=IntVar(self)
        self.wzcount=IntVar(self)
        self.zdcount0=IntVar(self)
        self.zdcount1=IntVar(self)
        self.cids=-1
        self.getCount()
        self.createWidgets()

    def createWidgets(self):
        lframe=Frame(self)
        lframe.pack(side=LEFT,pady=6,padx=6)
        f0=Frame(lframe)
        f0.grid(row=0, column=0, sticky='w') # sticky='w'指定了组件在单元格中靠左对齐
        f1=Frame(lframe)
        f1.grid(row=1, column=0, sticky='w')
        f2=Frame(lframe)
        f2.grid(row=2, column=0, sticky='w')
        Label(f0,text='网址总数:').pack(padx=3,side=LEFT)
        Label(f0,textvariable=self.alcount).pack(padx=3,side=LEFT)
        Label(f1,text='当前未采集:').pack(padx=3,side=LEFT)
        Label(f1,textvariable=self.cjcount,fg='red').pack(padx=3,side=LEFT)
        Label(f2,text='当前内容总数:').pack(padx=3,side=LEFT)
        Label(f2,textvariable=self.wzcount,fg='red').pack(padx=3,side=LEFT)

        lbframe=Frame(self)
        lbframe.pack(side=LEFT,padx=6,pady=6)
        f3=Button(lbframe,text='刷新数据',command=self.rload_data)
        f3.grid(row=0, column=0, sticky='w',pady=3)
        f4=Button(lbframe,text='全部采集',command=self.cj_cot)
        f4.grid(row=1, column=0, sticky='w',pady=3)

        ttk.Separator(self,orient='vertical').pack(side=LEFT,fill=Y,padx=10)

        rframe=Frame(self)
        rframe.pack(side=LEFT,padx=6,pady=6)
        f5=Frame(rframe)
        f5.grid(row=1, column=0, sticky='w') # sticky='w'指定了组件在单元格中靠左对齐
        f6=Frame(rframe)
        f6.grid(row=2, column=0, sticky='w')
        f8=Frame(rframe)
        f8.grid(row=0, column=0, sticky='w')
        Label(f5,text='网址总数:').pack(padx=3,side=LEFT)
        Label(f5,textvariable=self.zdcount0).pack(padx=3,side=LEFT)
        Label(f6,text='网址未采集:').pack(padx=3,side=LEFT)
        Label(f6,textvariable=self.zdcount1,fg='red').pack(padx=3,side=LEFT)
        Label(f8, text='输入cid:').pack(side=LEFT, padx=3)
        self.zdinp=Entry(f8,width=10)
        self.zdinp.pack(side=LEFT,padx=3, pady=3)
        rbFrame=Frame(self)
        rbFrame.pack(side=LEFT,padx=6,pady=6)

        f9=Button(rbFrame,text='刷新数据',command=self.rload_data2)
        f9.grid(row=0, column=0, sticky='w',pady=3)
        f10=Button(rbFrame,text='指定采集',command=self.cj_cot2)
        f10.grid(row=1, column=0, sticky='w',pady=3)

        ttk.Separator(self,orient='vertical').pack(side=LEFT,fill=Y,padx=10)

        Label(self, text='并发数:').pack(side=LEFT, padx=5, pady=2)
        self.typeSelect = ttk.Combobox(self,width=5,state='readonly')
        self.typeSelect['value']=[1,2,3,4,5]
        self.typeSelect.pack(side=LEFT, padx=2, pady=2)
        self.typeSelect.current(2)

        


    
    def getCount(self):
        res0=exe_sql('select count(id) from pids')
        res1=exe_sql('select count(id) from pids where pstate=0')
        res2=exe_sql('select count(id) from product')
        self.alcount.set(res0[0][0])
        self.cjcount.set(res1[0][0])
        self.wzcount.set(res2[0][0])
    
    def cj_cot(self):
        try:
            self.cids=-1
            bfs=int(self.typeSelect.get())
            res=asyncio.run(begin_cj_content(w,h,bfs,cids=self.cids))
            if not res:
                messagebox.showerror('错误','采集失败请重试')

            else:
                self.getCount()
                messagebox.showinfo('提示',f'采集完成,数据库目前有{self.wzcount.get()}个产品')

        except Exception as e:

            print(f'cj_cot => {e}')
    
    def cj_cot2(self):
        try:
            if self.cids==-1:
                messagebox.showerror('错误','请先获取数据')
                return
            bfs=int(self.typeSelect.get())
            res=asyncio.run(begin_cj_content(w,h,bfs,cids=self.cids))
            if not res:
                messagebox.showerror('错误','采集失败请重试')

            else:
                self.rload_data2()
                messagebox.showinfo('提示',f'采集完成,数据库目前有{self.wzcount.get()}个产品')

        except Exception as e:

            print(f'cj_cot2 => {e}')
    

    def rload_data(self):
        self.getCount()

    def rload_data2(self):
        cids_str=self.zdinp.get()
        if not cids_str:
            messagebox.showerror('错误','请输入数据')
            return
        where=f'({cids_str})'
        self.cids=where
        res0=exe_sql(f'select count(id) from pids where pcid in {where}')
        res1=exe_sql(f'select count(id) from pids where pcid in {where} and pstate=0')
        self.zdcount0.set(res0[0][0])
        self.zdcount1.set(res1[0][0])

obcot=CotFra(master=root)

ttk.Separator(root,orient='horizontal').pack(fill=X,pady=5)

if __name__=='__main__':

    root.mainloop()