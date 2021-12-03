from tkinter import Button, Entry,ttk
from sql import *
import tkinter as tk
import tkinter.messagebox as messagebox


def but():
    list_win=tk.Toplevel(bd=10)
    list_win.wm_geometry("600x400")
    list_win.title('类目处理')
    list_win.attributes('-topmost', True)
    tree = ttk.Treeview(list_win, show = "tree")
    root_nodes=select('grade=1','class')

    for j in range(len(root_nodes)):
        cur_cid=root_nodes[j]['cid']
        tree.insert("",j,f'{cur_cid}',text=root_nodes[j]['cname'],values=(cur_cid,))
        child_nodes=select(f'grade=2 and cfid={cur_cid}','class')
        for k in range(len(child_nodes)):
            tree.insert(f'{cur_cid}',k,f"{child_nodes[k]['cid']}",text=f"{child_nodes[k]['cname']} ({child_nodes[k]['cid']})",values=(cur_cid,child_nodes[k]['cid']))

    popup_menu = tk.Menu(list_win, tearoff=0)


    def show_tc(fcid):
        tc=tk.Toplevel(bd=10)
        tc.wm_geometry("300x200")
        tc.title('上传类目')
        tc.attributes('-topmost',True)
        en=Entry(tc)
        en.pack(pady=10)
        def upkw():
            if fcid:
                obj={'cfid':fcid,'cname':en.get().strip(),'grade':2}
            
            else:
                obj={'cname':en.get().strip(),'grade':1}
            
            insert([obj],'class')
            list_win.attributes('-topmost', False)
            messagebox.showinfo('提示','操作完成')
            list_win.attributes('-topmost', True)
            tc.destroy()
            list_win.destroy()
            but()
        Button(tc,text='上传',command=upkw).pack()
        

    def add_root():
        show_tc(fcid=None)

    def add_item():
        item=tree.focus()
        fcid=int(tree.item(item,'values')[0])
        show_tc(fcid)
    
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
            delete(f'cid={vals[1]}','class')
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
            #print(item_text)

    def popup(event):
        try:
            popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:                                                                                                                                                                                                                                                                                       
            popup_menu.grab_release()

    # 选中行
    tree.bind('<<TreeviewSelect>>', selectTree)
    tree.bind('<Button-3>',popup)

    tree.pack(expand = True,fill='both')


# root=tk.Tk()
# root.title('GUI')#标题
# root.geometry('800x600')#窗体大小
# root.resizable(False, False)#固定窗体
# f = tk.Button(root,text='子窗体',command=but).pack()
# root.mainloop()