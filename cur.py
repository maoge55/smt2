from tkinter import Button, Entry,ttk
from sql import *
import tkinter as tk
import tkinter.messagebox as messagebox
import lua.tocn as fyss
import json,time

lang=0
def but():

    list_win=tk.Toplevel(bd=10)
    list_win.wm_geometry("600x400")
    list_win.title('类目处理')


    def yjfy():
        global lang

        if not lang:
            changlua(tree)
        else:
            list_win.destroy()
            but()
        lang=0 if lang else 1


    Button(list_win,text='一键翻译',command=yjfy).pack(pady=5)
    list_win.attributes('-topmost', True)
    tree = ttk.Treeview(list_win, show = "tree")
    root_nodes=select('grade=1','class')

    for j in range(len(root_nodes)):
        cur_cid=root_nodes[j]['cid']
        tree.insert("",j,f'{cur_cid}',text=f"{root_nodes[j]['cname']} ({root_nodes[j]['cid']})",values=(cur_cid,))
        child_nodes=select(f'grade=2 and cfid={cur_cid}','class')
        for k in range(len(child_nodes)):
            tree.insert(f'{cur_cid}',k,f"{child_nodes[k]['cid']}",text=f"{child_nodes[k]['cname']} ({child_nodes[k]['cid']})",values=(cur_cid,child_nodes[k]['cid']))
            cur_second_cid=child_nodes[k]['cid']
            third_nodes=select(f'grade=3 and cfid={cur_second_cid}','class')
            for k2 in range(len(third_nodes)):
                tree.insert(f'{cur_second_cid}',k2,f"{third_nodes[k2]['cid']}",text=f"{third_nodes[k2]['cname']} ({third_nodes[k2]['cid']})",values=(cur_cid,cur_second_cid,third_nodes[k2]['cid']))


    popup_menu = tk.Menu(list_win, tearoff=0)

    def show_tc(itm):
        tc=tk.Toplevel(bd=10)
        tc.wm_geometry("300x200")
        tc.title('上传类目')
        tc.attributes('-topmost',True)
        en=Entry(tc)
        en.pack(pady=10)
        def upkw():
            sj_category=(str(int(time.time()*1000)))[5:]
            if not itm:
                obj = {
                    'cname': en.get().strip(), 
                    'grade': 1,
                    'category':sj_category,
                    'isup': 1
                }
            else:
                vals=tree.item(itm, "values")
                fcid=int(vals[-1])
                respp=select(f'cid={fcid}','class')
                cfname=respp[0]['cname']
                obj = {
                    'cname': en.get().strip(),
                    'grade': len(vals)+1,
                    'cfid': fcid,
                    'category':sj_category,
                    'fidlist':json.dumps([int(val) for val in vals]),
                    'cfname':cfname,
                    'isup': 1,
                }
            print(obj)
            res=insert([obj],'class')
            print(res)
            list_win.attributes('-topmost', False)
            messagebox.showinfo('提示','操作完成')
            list_win.attributes('-topmost', True)
            tc.destroy()
            list_win.destroy()
            but()
        Button(tc,text='上传',command=upkw).pack()
        

    def add_root():
        show_tc(itm=None)

    def add_item():
        item=tree.focus()
        show_tc(item)
    
    def delete_selected():
        item=tree.focus()
        list_win.attributes('-topmost', False)
        vals=tree.item(item, "values")
        if len(list(vals))<=1:
            messagebox.showerror('删除失败',f'《{tree.item(item,"text")}》是根节点不可删除')
            list_win.attributes('-topmost', True)
            return
        res=messagebox.askyesno('确认删除',f'是否确定删除《{tree.item(item,"text")}》节点')
        if res:
            delete(f'cid={vals[-1]}','class')
            tree.delete(item)
        list_win.attributes('-topmost', True)

    popup_menu.add_command(label="添加根节点",command=add_root)
    popup_menu.add_command(label="添加子节点",command=add_item)
    popup_menu.add_command(label="删除节点",command=delete_selected)

    # 鼠标选中一行回调
    def selectTree(event):
        pass
        # for item in tree.selection():
        #     item_text = tree.item(item, "values")
        #     print(item_text)

    def popup(event):
        try:
            popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:                                                                                                                                                                                                                                                                                       
            popup_menu.grab_release()

    # 选中行
    tree.bind('<<TreeviewSelect>>', selectTree)
    tree.bind('<Button-3>',popup)

    tree.pack(expand = True,fill='both')

def changlua(t):
    entxts=[]
    for it0 in t.get_children():
        entxts.append(t.item(it0,'text'))
        for it1 in t.get_children(it0):
            entxts.append(t.item(it1,'text'))
            for it2 in t.get_children(it1):
                entxts.append(t.item(it2,'text'))

    cntxts=[]
    for jj in range(len(entxts)//200+1):
        st=jj*200;ed=(jj+1)*200
        cntxts.extend(fyss.fy('\n'.join(entxts[st:ed])))
    
    ind=0
    for it0 in t.get_children():
        t.item(it0,text=cntxts[ind])
        ind+=1
        for it1 in t.get_children(it0):
            t.item(it1,text=cntxts[ind])
            ind+=1
            for it2 in t.get_children(it1):
                t.item(it2,text=cntxts[ind])
                ind+=1
    

# root=tk.Tk()
# root.title('GUI')#标题
# root.geometry('800x600')#窗体大小
# root.resizable(False, False)#固定窗体
# f = tk.Button(root,text='子窗体',command=but).pack()
# root.mainloop()
