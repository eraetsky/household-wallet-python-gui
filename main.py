import tkinter as tk
import tkinter.font as font
from tkinter import ttk
import sqlite3
import matplotlib.pyplot as plt



class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        main_font = font.Font(family="Arial", size=12, weight="bold")

        toolbar = tk.Frame(bg="#32CD32", bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        footer = tk.Frame(bg="#008000", bd=2)
        footer.pack(side=tk.BOTTOM, fill=tk.X)

        self.db = db
        self.db.c.execute('''SELECT SUM(cost) FROM finance''')
        result = self.db.c.fetchone()[0]
        s_balance = "Текущий баланс: " + str(result)

        label_balance = tk.Label(footer, bg="#008000",text=s_balance)
        label_balance["font"] = main_font
        label_balance.pack(side=tk.LEFT)

        self.add_img = tk.PhotoImage(file="add.gif")
        btn_open_dialog = tk.Button(toolbar, text="Добавить позицию", command=self.open_dialog, bg="#d7d8e0",
                                    width=170,bd=0, compound=tk.TOP, image=self.add_img)
        btn_open_dialog["font"] = main_font
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file="update.gif")
        btn_edit_dialog = tk.Button(toolbar, text="Редактировать", bg="#d7d8e0", bd=0, image=self.update_img,
                                    width=100, compound=tk.TOP, command=self.open_update_dialog)
        btn_edit_dialog["font"] = main_font
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file="delete.gif")
        btn_delete = tk.Button(toolbar, text="Удалить позицию", bg="#d7d8e0", bd=0, image=self.delete_img,
                               width=120,compound=tk.TOP, command=self.delete_records)
        btn_delete["font"] = main_font
        btn_delete.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file="search.gif")
        btn_search = tk.Button(toolbar, text="Поиск", bg="#d7d8e0", bd=0, image=self.search_img,
                               compound=tk.TOP, command=self.open_search_dialog)
        btn_search["font"] = main_font
        btn_search.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file="refresh.gif")
        btn_refresh = tk.Button(toolbar, text="Обновить", bg="#d7d8e0", bd=0, image=self.refresh_img,
                                compound=tk.TOP, command=self.view_records)
        btn_refresh["font"] = main_font
        btn_refresh.pack(side=tk.LEFT)

        self.extract_img = tk.PhotoImage(file="extract.gif")
        btn_extract = tk.Button(toolbar, text="Аналитика", bg="#d7d8e0", bd=0, image=self.extract_img,
                                width=150,compound=tk.TOP, command=self.open_extract_dialog)
        btn_extract["font"] = main_font
        btn_extract.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=("ID", "description", "cost", "total"), height=15,
                                 show="headings")
        self.tree.column("ID", width=160, anchor=tk.CENTER)
        self.tree.column("description", width=160, anchor=tk.CENTER)
        self.tree.column("cost", width=160, anchor=tk.CENTER)
        self.tree.column("total", width=160, anchor=tk.CENTER)

        self.tree.heading("ID", text="ID")
        self.tree.heading("description", text="Наименование")
        self.tree.heading("cost", text="Сумма")
        self.tree.heading("total", text="Доход/расход")

        self.tree.pack(side=tk.LEFT)

        scr_bar = tk.Scrollbar(self, command=self.tree.yview)
        scr_bar.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scr_bar.set)

    def records(self, description, cost, total):
        self.db.insert_data(description, cost, total)
        self.view_records()

    def update_record(self, description, cost, total):
        self.db.c.execute('''UPDATE finance SET description = ?, cost = ?, total = ? WHERE ID = ?''',
                          (description, cost, total, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM finance''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', "end", values=row) for row in self.db.c.fetchall()]

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM finance WHERE id = ?''', (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

    def search_records(self, description):
        description = ('%' + description + '%',)
        self.db.c.execute('''SELECT * FROM finance WHERE description LIKE ?''', description)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', "end", values=row) for row in self.db.c.fetchall()]

    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()

    def open_search_dialog(self):
        Search()

    def open_extract_dialog(self):
        Extract()


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title("Добавить доходы или расходы")
        self.geometry("450x220+400+300")
        self.resizable(0, 0)

        label_description = tk.Label(self, text="Наименование:")
        label_description.place(x=20, y=50)
        label_select = tk.Label(self, text="Статья дохода/расхода:")
        label_select.place(x=20, y=80)
        label_sum = tk.Label(self, text="Сумма:")
        label_sum.place(x=20, y=110)

        self.entry_description = ttk.Entry(self)
        self.entry_description.place(x=200, y=50)

        self.entry_money = ttk.Entry(self)
        self.entry_money.place(x=200, y=110)

        self.combobox = ttk.Combobox(self, values=[u"Доход", u"Расход"], state="readonly")
        self.combobox.current(0)
        self.combobox.place(x=200, y=80)
        def expenses_selected(event):
            if self.combobox.get() == "Доход":
                self.entry_money.delete(0)
                self.entry_money.insert(0,'-')
        self.combobox.bind("<Button-1>", expenses_selected)

        btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        btn_cancel.place(x=310, y=170)
        self.btn_ok = ttk.Button(self, text="Добавить")
        self.btn_ok.place(x=200, y=170)
        self.btn_ok.bind("<Button-1>", lambda event: self.view.records(self.entry_description.get(),
                                                                       self.entry_money.get(),
                                                                       self.combobox.get()))

        self.grab_set()
        self.focus_set()


class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title("Редактировать позицию")
        btn_edit = ttk.Button(self, text="Редактировать")
        btn_edit.place(x=170, y=170)
        btn_edit.bind("<Button-1>", lambda event: self.view.update_record(self.entry_description.get(),
                                                                          self.entry_money.get(), self.combobox.get()))
        self.btn_ok.destroy()

    def default_data(self):
        self.db.c.execute('''SELECT * FROM finance WHERE id=?''',
                          (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_description.insert(0, row[1])
        if row[3] != "Доход":
            self.combobox.current(1)
        self.entry_money.insert(0, row[2])


class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title("Поиск")
        self.geometry("300x100+400+300")
        self.resizable(0, 0)

        label_search = tk.Label(self, text="Поиск")
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text="Поиск")
        btn_search.place(x=85, y=50)
        btn_search.bind("<Button-1>", lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind("<Button-1>", lambda event: self.destroy(), add='+')


class Extract(tk.Toplevel):
    def __init__(self):
        self.db = db
        self.init_extract()

    def init_extract(self):

        self.db.c.execute('''SELECT SUM(cost) FROM finance WHERE cost > 0''')
        income = self.db.c.fetchone()[0]
        s_income = "Доходы: " + str(income)

        self.db.c.execute('''SELECT SUM(cost) FROM finance WHERE cost < 0''')
        outcome = self.db.c.fetchone()[0]
        s_outcome = "Расходы: " + str(outcome)

        self.db.c.execute('''SELECT SUM(cost) FROM finance''')
        balance = self.db.c.fetchone()[0]
        s_total = "Баланс: " + str(balance)

        categories = "Продукты", "Кафе и рестораны", "Здоровье и красота", "Услуги", "Другое"
        self.db.c.execute('''SELECT SUM(cost) FROM finance WHERE description == "Продукты"''')
        food = self.db.c.fetchone()[0] or 0
        food *= -1
        self.db.c.execute('''SELECT SUM(cost) FROM finance WHERE description == "Ресторан" 
                            OR description == "Кафе"''')
        restaurants = self.db.c.fetchone()[0] or 0
        restaurants *= -1
        self.db.c.execute('''SELECT SUM(cost) FROM finance WHERE description == "Аптека" 
                            OR description == "Здоровье и красота"
                            OR description == "Здоровье"''')
        health = self.db.c.fetchone()[0] or 0
        health *= -1
        self.db.c.execute('''SELECT SUM(cost) FROM finance WHERE description == "Услуги"''')
        services = self.db.c.fetchone()[0] or 0
        services *= -1
        other = (-outcome) - food - restaurants - health - services

        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        labels = categories
        sizes = [food, restaurants, health, services, other]
        explode = (0, 0, 0, 0, 0)
        fig1, ax1 = plt.subplots(figsize=(10,10))
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.legend(loc='best', bbox_to_anchor=(0.5, 0.6, 0.6, 0.5))
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.text(-0.4,-1.15,s_outcome, fontsize=15)
        plt.text(-0.4, -1.25, s_income, fontsize=15)
        plt.text(-0.4, -1.35, s_total, fontsize=15)
        plt.show()


class DB:
    def __init__(self):
        self.conn = sqlite3.connect("finance.db")
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS finance (id integer primary key, description text, cost text, total real) '''
        )
        self.conn.commit()

    def insert_data(self, description, cost, total):
        self.c.execute('''INSERT INTO finance(description, cost,total) VALUES (?,?,?)''',
                       (description, cost, total))
        self.conn.commit()


if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Wallet")
    root.geometry("665x450+300+200")
    root.resizable(False, False)
    root.mainloop()
