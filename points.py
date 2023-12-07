# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 07:28:26 2023

Version 2. Making use of ttk, a much better GUI, and more accurate math.

@author: i-JL
"""

from tkinter import *
from tkinter import ttk

def key_press(e):
    cal_output()
    update_odds(e)
    
def key_release(e):
    update_odds(e)
    cal_output()

def cal_output():
    exact_label.config(style='Positive.TLabel')
    rounded_label.config(style='Positive.TLabel')
        
    confidence_level = current_confidence.get() / 100
    points = int(float(pointsinput.get()))
    max_value = points * 0.2
    points_on_win  = int(float(winput.get()))
    points_on_loss = int(float(loseput.get()))
    winloss_sum = points_on_win + points_on_loss    
    
    # Values fixed for arbitrary reasons
    win_percent = 0.6
    loss_percent = 0.4
    win_returns =  points_on_win / winloss_sum
    loss_returns = points_on_loss / winloss_sum 
    kelly_criterion = (win_percent / loss_returns) - (loss_percent / win_returns)

    exact_label_value = points * kelly_criterion
    
    exact_label_value *= confidence_level
    exact_label.config(text=exact_label_value)
    rounded_label_value = round(exact_label_value)
        
    if abs(round(exact_label_value)) <= max_value:
        rounded_label_value = abs(round(exact_label_value)) 
    else:
        rounded_label_value = round(max_value)
    
    if exact_label_value < 0:
        exact_label.config(style='Negative.TLabel')
        rounded_label.config(style='Negative.TLabel')

    rounded_label.config(text=rounded_label_value)

def update_confidence_label(currconf):
    conf_label['text'] = f'{int(float(currconf)):3}%'
    cal_output()
    
def update_odds(currodds):
    points_on_win  = int(float(winput.get()))
    points_on_loss = int(float(loseput.get()))
    winloss_sum = points_on_win + points_on_loss
    odds_bar.config(to=winloss_sum)
    current_odds.set(points_on_win)
    winloss_percent = int(( points_on_win / winloss_sum ) * 100)
    odds_label['text'] = f'{winloss_percent:3}%'
    
win=Tk()

# Configure general settings
w = 455
h = 160
ws = win.winfo_screenwidth()
hs = win.winfo_screenheight()
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

win.geometry('%dx%d+%d+%d' % (w, h, x, y))
win.grid_anchor(anchor='center')
win.iconbitmap("C:/Users/admin/lanayaya.ico")
win.title("Points Calculator")
win['background']='#36393e'

# General style settings
style=ttk.Style()
style.theme_settings("default", {
    "Column": {"Stretch": False}
})

# Widget-specific style settings
style.configure("TEntry", foreground="#1e2124", background="#36393e", relief="sunken")
style.configure("Info.TLabel", foreground="white", background="#1e2124",font="TkFixedFont",relief="sunken",reliefcolor="red")
style.configure(".", foreground="white", background="#36393e")
style.configure("Odds.Horizontal.TScale")
style.configure("Positive.TEntry",foreground="#387aff")
style.configure("Negative.TEntry",foreground="#f5009b")
style.configure("Positive.TLabel",foreground="#387aff")
style.configure("Negative.TLabel",foreground="#f5009b")

# Row 0: Input
pointsinput=ttk.Entry(win, width=30)
pointsinput.grid(row=0,column=1)

# Rows 1 & 2: Displays
rounded_label = ttk.Label(win, text="(Enter current points)", font=('Calibri 15 bold'))
rounded_label.grid(row=1,column=1)

exact_label = ttk.Label(win, text="(Non-rounded result)", font=('Calibri 8'))
exact_label.grid(row=2,column=1)

# Row 3: Confidence
conftext_label=ttk.Label(win,text="Confidence: ")
conftext_label.grid(row=3,column=0)

current_confidence=IntVar()
scale_bar = ttk.Scale(
    win, 
    from_=0, 
    to=100, 
    length=200,
    variable=current_confidence, 
    command=update_confidence_label
)
current_confidence.set(100)
scale_bar.grid(row=3,column=1)

conf_label=ttk.Label(win,text=f'{current_confidence.get()}'+'%',style="Info.TLabel")
conf_label.grid(row=3,column=2)

# Row 4: Labels for context
win_label=ttk.Label(win,text='Points on win',style="Positive.TLabel")
win_label.grid(row=4,column=0)

loss_label=ttk.Label(win,text='Points on loss',style="Negative.TLabel")
loss_label.grid(row=4,column=2)

# Row 5: Other totals and scale for visualization
winput=ttk.Entry(win, style="Positive.TEntry")
winput.grid(row=5,column=0)

loseput=ttk.Entry(win, style="Negative.TEntry")
loseput.grid(row=5,column=2)

current_odds=IntVar()
odds_bar = ttk.Scale(
    win, 
    from_=0, 
    to=100, 
    length=200,
    variable=current_odds, 
    command=update_odds,
    style="Odds.Horizontal.TScale"
)
odds_bar.grid(row=5,column=1)
odds_bar['state']=DISABLED

# Row 6: Display for row 5
odds_label=ttk.Label(win,text='?%',style="Info.TLabel")
odds_label.grid(row=6,column=1)

win.bind('<KeyPress>',key_press)
win.bind('<KeyRelease>',key_release)

win.mainloop()
