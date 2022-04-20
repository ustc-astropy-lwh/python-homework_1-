from datetime import datetime
from utils import *
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

class GUI():
    def __init__(self):
        self.code = None
        self.dayfrom = None
        self.dayto = None

    def create_main(self):
        # create main GUI
        root = Tk()
        root.title("stock data extract")    # GUI title
        root.configure(bg="lightblue")    # GUI background color
        self.screenwidth = root.winfo_screenwidth()    # screen width
        self.screenheight = root.winfo_screenheight()    #  screen height
        self.w,self.h = 820,520    # GUI width,height
        root.geometry("%dx%d+%d+%d" % (self.w,self.h,(self.screenwidth-self.w)/2,(self.screenheight-self.h)/2))    # GUI position

        # Button
        button1 = Button(root,text="Search",width=40,command=self.createNewWindow)    # search stock in a newWindow
        button_end = Button(root,text="Exit",width=40,command=root.destroy)    # exit
        button1.pack()
        button_end.pack()

        # picture
        html_png = PhotoImage(file=r"E:\中科大学习\大三课程\python与深度学习基础\大作业1\1.png")    
        label2 = Label(root,text="""红专并进，理实交融""",image=html_png,bg="lightyellow",compound="bottom",font=("Helvetic",20,"bold"),cursor="star") 
        label2.pack(pady=20)

        root.mainloop()

    def createNewWindow(self):
        newWindow = Toplevel()    # create new window when I click "search"
        newWindow.title("stock data extract")    # newWindow title
        newWindow.configure(bg="lightblue")    # newWindow background color
        newWindow.geometry("%dx%d+%d+%d" % (self.w,self.h,(self.screenwidth-self.w)/2,(self.screenheight-self.h)/2))    # newWindow position

        b_shanghai = Button(newWindow,text="1.Shanghai Securities Composite Shares",font=("Helvetic",20,"bold"),command=lambda:self.get_a_stock(".SS"))
        b_shanghai.pack(fill=X)
        b_shenzhen = Button(newWindow,text="2.Shenzhen Securities Composite Shares",font=("Helvetic",20,"bold"),command=lambda:self.get_a_stock(".SZ"))
        b_shenzhen.pack(fill=X)
        # b_hkong = Button(newWindow,text="3.Hong Kong Securities Composite Shares",font=("Helvetic",20,"bold"),command=lambda:self.get_a_stock(".HK"))
        # b_hkong.pack(fill=X)
        b_end = Button(newWindow,text="Return main interface",font=("Helvetic",20,"bold"),command=newWindow.destroy)    # Return root 
        b_end.pack(anchor=S,fill=X)

    def get_a_stock(self,suffix): 
        self.suffix = suffix 
        # sub 
        sub = Toplevel()    # create new window 
        sub.title("stock data extract")    # title
        sub.configure(bg="lightblue")    # background color
        sub.geometry("320x250+%d+%d" % ((self.screenwidth-self.w)/2,(self.screenheight-self.h)/2))

        # sub label for stock code, day from, day to
        code_label = Label(sub,text="stock code")
        code_label.grid(row=0)
        day_from_label = Label(sub,text="day from")
        day_from_label.grid(row=1)
        day_to_label = Label(sub,text="day to")
        day_to_label.grid(row=2)
        remind = Label(sub,text="Please enter a day like: 2022-04-18")
        remind.grid(row=5,columnspan=2)

        # sub Entry 
        self.en1 = StringVar()
        self.en2 = StringVar()
        self.en3 = StringVar()
        code_entry = Entry(sub,textvariable=self.en1)
        code_entry.grid(row=0,column=1)
        day_from_entry = Entry(sub,textvariable=self.en2)
        day_from_entry.grid(row=1,column=1,pady=10)
        day_to_entry = Entry(sub,textvariable=self.en3)
        day_to_entry.grid(row=2,column=1)

        # class create
        self.stock = get_stock_historical_data()

        # login 
        exit_ = Button(sub,text="Return last interface",command=sub.destroy)
        exit_.grid(row=3,column=1,pady=10)
        login = Button(sub,text="go",command=self.login_entry)
        login.grid(row=3,column=0)

    def login_entry(self):
        # get entry
        self.code = self.en1.get()
        self.dayfrom = self.en2.get()
        self.dayto = self.en3.get()
        # get suffix
        self.stock.get_stocktype(suffix=self.suffix)
        # get stock code
        self.stock.get_stock_code(code=self.code)
        # get day from
        self.stock.get_dayfrom(dayfrom=self.dayfrom)
        # get day to
        self.stock.get_dayto(dayto=self.dayto)

        try:
            # start extract
            self.data, self.text = self.stock.get_SS()
            # sub_new 
            sub_new = Toplevel()    # create new window 
            sub_new.title("stock data show")    # title
            sub_new.configure(bg="lightblue")    # background color
            sub_new.geometry("%dx%d+%d+%d" % (self.w,self.h,(self.screenwidth-self.w)/2,(self.screenheight-self.h)/2))
            # plot data button
            plot_button = Button(sub_new,text="plot data",command=self.draw_data)
            plot_button.pack(pady=5)
            # return last interface
            break_button = Button(sub_new,text="return last interface",command=sub_new.destroy)
            break_button.pack(pady=5)
            # create scrollbar and text
            scrollbar = Scrollbar(sub_new)
            scrollbar.pack(side=RIGHT,fill=Y)
            text = Text(sub_new,width=self.w,height=self.h)
            text.pack()
            scrollbar.config(command=text.yview)    # set text roll with scrollbar
            text.config(yscrollcommand=scrollbar.set)
            # insert data
            text.insert(END,self.text)

        except:
            # sub_new 
            sub_new = Toplevel()    # create new window 
            sub_new.title("extract failed")    # title
            sub_new.configure(bg="red")    # background color
            sub_new.geometry("270x150+%d+%d" % ((self.screenwidth-self.w)/2,(self.screenheight-self.h)/2))
            label_error = Label(sub_new,text="no data/error occur")    # error minder
            label_error.pack(anchor=CENTER,pady=10)
            button_error = Button(sub_new,text="Return last interface",command=sub_new.destroy)    # return last interface
            button_error.pack()

    def draw_data(self):
        # sub_plot 
        sub_plot = Toplevel()    # create new window 
        sub_plot.title("stock data plot")    # title
        sub_plot.configure(bg="lightblue")    # background color
        # sub_plot.geometry("%dx%d+%d+%d" % (self.w,self.h,(self.screenwidth-self.w)/2,(self.screenheight-self.h)/2))
        
        # figure
        # I don't know why all of my windows size will change after "plot"
        fig, ax= plt.subplots(5,figsize=(10,6))
        fig.suptitle('Date')    # share x axis

        # date axis
        date_axis = self.data['Date']
        dates = [datetime.strptime(d, '%Y-%m-%d').date() for d in date_axis]
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator())
        # open
        ax[0].set_xticks(dates[::int(len(date_axis)/5.)])    # scale
        ax[0].set_ylabel('Open')
        ax[0].plot(dates,self.data['Open'],'blue')    # plot
        # high
        ax[1].set_xticks(dates[::int(len(date_axis)/5.)])    # scale
        ax[1].set_ylabel('High')
        ax[1].plot(dates,self.data['High'],'red')    # plot
        # low
        ax[2].set_xticks(dates[::int(len(date_axis)/5.)])    # scale
        ax[2].set_ylabel('Low')
        ax[2].plot(dates,self.data['Low'],'green')    # plot
        # close
        ax[3].set_xticks(dates[::int(len(date_axis)/5.)])    # scale
        ax[3].set_ylabel('Close')
        ax[3].plot(dates,self.data['Close'],'grey')    # plot
        # volume
        ax[4].set_xticks(dates[::int(len(date_axis)/5.)])    # scale
        ax[4].set_ylabel('Volume')
        ax[4].plot(dates,self.data['Volume'])    # plot
        plt.gcf().autofmt_xdate()  # rotota date

        # canvas
        canvas = FigureCanvasTkAgg(fig, sub_plot)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP,fill=BOTH,expand=YES)
        # matplotlib guide tool
        toolbar = NavigationToolbar2Tk(canvas,sub_plot)
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP,fill=BOTH,expand=YES)
        # exit
        e_button = Button(sub_plot,text="exit plot",command=sub_plot.destroy)
        e_button.pack(side=TOP)


if __name__ == "__main__":
    a = GUI()
    a.create_main()
