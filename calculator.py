import re
import tkinter as tk
import math

# 创建窗口
root = tk.Tk()
root.geometry('480x400+150+150')
root.title('计算器')
root.attributes('-alpha', 1.0)
root['background'] = '#ffffff'

# 准备
lists = []
result_num = tk.StringVar()
result_num.set('0')
stored_result = None
xinjisuan = False

# 按下数字
def append_num(i):
    global xinjisuan
    if xinjisuan:
        lists.clear()
        xinjisuan = False
    lists.append(i)
    result_num.set(''.join(lists))

# 按下运算符号
def yunsuan(i):
    global xinjisuan
    if xinjisuan:
        xinjisuan = False
    if len(lists) > 0 and lists[-1] not in ['+', '-', 'x', '÷']:
        lists.append(i)
        result_num.set(''.join(lists))

# 等于
def equal():
    global stored_result
    expression = ''.join(lists).replace('x', '*').replace('÷', '/')
    if re.search(r'[\+\-\*/]{2,}', expression):
        result_num.set('错误')
        lists.clear()
    else:
        try:
            end_num = eval(expression)
            result_num.set(end_num)
            lists.clear()
            stored_result = str(end_num)
            lists.append(stored_result)
        except ZeroDivisionError:
            result_num.set('错误')
            lists.clear()
        except Exception:
            result_num.set('错误')
            lists.clear()

# 清除
def clear():
    global stored_result, xinjisuan
    lists.clear()
    result_num.set('0')
    stored_result = None
    xinjisuan = False

# 退格
def back():
    if lists:
        lists.pop()
        if lists:
            result_num.set(''.join(lists))
        else:
            result_num.set('0')

# 平方根
def sqrt():
    global stored_result, xinjisuan
    if lists:
        try:
            num = float(''.join(lists))
            result = math.sqrt(num)
            result_num.set(result)
            lists.clear()
            stored_result = str(result)
            lists.append(stored_result)
            xinjisuan = True
        except ValueError:
            result_num.set('错误')
            lists.clear()

# 取余
def quyu():
    if len(lists) > 0 and lists[-1] not in ['+', '-', 'x', '÷', '%']:
        lists.append('%')
        result_num.set(''.join(lists))

# 倒数
def daoshu():
    global stored_result, xinjisuan
    if lists:
        try:
            num = float(''.join(lists))
            result = 1 / num
            result_num.set(result)
            lists.clear()
            stored_result = str(result)
            lists.append(stored_result)
            xinjisuan = True
        except ZeroDivisionError:
            result_num.set('错误')
            lists.clear()

# 归零
def guiling():
    global stored_result
    result_num.set('0')
    lists.clear()
    stored_result = None

# 正负号转换
def zhengfu():
    if lists:
        if lists[0] == '-':
            lists.pop(0)
        else:
            lists.insert(0, '-')
        result_num.set(''.join(lists))

# 创建贷款计算器窗口
def open_loan_calculator():
    loan_window = tk.Toplevel(root)
    loan_window.title("贷款计算器")
    loan_window.geometry("400x300")

    tk.Label(loan_window, text="贷款金额(万元):").grid(row=0, column=0)
    tk.Label(loan_window, text="年利率 (%):").grid(row=1, column=0)
    tk.Label(loan_window, text="贷款年限(年):").grid(row=2, column=0)
    tk.Label(loan_window, text="还款方式:").grid(row=3, column=0)

    amount_entry = tk.Entry(loan_window)
    rate_entry = tk.Entry(loan_window)
    years_entry = tk.Entry(loan_window)
    repayment_method = tk.StringVar(value='等额本息')

    amount_entry.grid(row=0, column=1)
    rate_entry.grid(row=1, column=1)
    years_entry.grid(row=2, column=1)
    tk.Radiobutton(loan_window, text="等额本息", variable=repayment_method, value="等额本息").grid(row=3, column=1, sticky='w')
    tk.Radiobutton(loan_window, text="等额本金", variable=repayment_method, value="等额本金").grid(row=3, column=1, padx=100, sticky='w')

    # 创建结果显示标签
    monthly_payment_label = tk.Label(loan_window, text="每月还款额: ")
    monthly_payment_label.grid(row=4, column=0, columnspan=2, sticky='w')

    total_interest_label = tk.Label(loan_window, text="利息总额: ")
    total_interest_label.grid(row=5, column=0, columnspan=2, sticky='w')

    total_payment_label = tk.Label(loan_window, text="还款总额: ")
    total_payment_label.grid(row=6, column=0, columnspan=2, sticky='w')

    # 计算贷款
    def calculate_loan():
        try:
            principal = float(amount_entry.get()) * 10000
            annual_rate = float(rate_entry.get()) / 100
            years = int(years_entry.get())
            monthly_rate = annual_rate / 12
            num_payments = years * 12

            if repayment_method.get() == '等额本息':
                monthly_payment = (principal * monthly_rate * math.pow(1 + monthly_rate, num_payments)) / \
                                  (math.pow(1 + monthly_rate, num_payments) - 1)
                total_payment = monthly_payment * num_payments
                total_interest = total_payment - principal
            else:
                monthly_payment = principal / num_payments + principal * monthly_rate
                total_payment = sum(principal / num_payments + (principal - (m - 1) * principal / num_payments) * monthly_rate for m in range(1, num_payments + 1))
                total_interest = total_payment - principal

            # 更新结果显示
            monthly_payment_label.config(text=f"每月还款额: {monthly_payment:,.2f}元")
            total_interest_label.config(text=f"利息总额: {total_interest:,.2f}元")
            total_payment_label.config(text=f"还款总额: {total_payment:,.2f}元")
        except ValueError:
            monthly_payment_label.config(text="输入无效，请重试。")
            total_interest_label.config(text="")
            total_payment_label.config(text="")

    # 计算按钮
    calculate_button = tk.Button(loan_window, text="计算", command=calculate_loan)
    calculate_button.grid(row=7, column=0, columnspan=1)

    # 重新计算按钮
    recalculate_button = tk.Button(loan_window, text="重新计算", command=lambda: [amount_entry.delete(0, 'end'), rate_entry.delete(0, 'end'), years_entry.delete(0, 'end'), monthly_payment_label.config(text="每月还款额: "), total_interest_label.config(text="利息总额: "), total_payment_label.config(text="还款总额: ")])
    recalculate_button.grid(row=7, column=1, columnspan=1)


# 创建主要显示屏
lable1 = tk.Label(root, textvariable=result_num, width=20, height=2, font=('YouYuan', 24), justify='left',
                  background='#ffffff', anchor='se')
lable1.grid(padx=4, pady=4, row=0, column=0, columnspan=4)

# 圆角按钮
def create_rounded_button(canvas, x1, y1, x2, y2, radius, text, command, color):
    rect1 = canvas.create_arc(x1, y1, x1 + 2 * radius, y1 + 2 * radius, start=90, extent=90, fill=color, outline=color)
    rect2 = canvas.create_arc(x2 - 2 * radius, y1, x2, y1 + 2 * radius, start=0, extent=90, fill=color, outline=color)
    rect3 = canvas.create_arc(x1, y2 - 2 * radius, x1 + 2 * radius, y2, start=180, extent=90, fill=color, outline=color)
    rect4 = canvas.create_arc(x2 - 2 * radius, y2 - 2 * radius, x2, y2, start=270, extent=90, fill=color, outline=color)
    rect5 = canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, fill=color, outline=color)
    rect6 = canvas.create_rectangle(x1, y1 + radius, x2, y2 - radius, fill=color, outline=color)
    button_text = canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=text, font=('YouYuan', 16),
                                     fill="black")
    button_items = [rect1, rect2, rect3, rect4, rect5, rect6]
    for item in button_items:
        canvas.tag_bind(item, '<ButtonPress-1>', lambda e, items=button_items: on_press(items))
        canvas.tag_bind(item, '<ButtonRelease-1>',
                        lambda e, items=button_items, c=color, cmd=command: on_release(items, cmd, c))
    canvas.tag_bind(button_text, '<ButtonPress-1>', lambda e, items=button_items: on_press(items))
    canvas.tag_bind(button_text, '<ButtonRelease-1>',
                    lambda e, items=button_items, c=color, cmd=command: on_release(items, cmd, c))

# 按下按钮效果
def on_press(items):
    for item in items:
        canvas.itemconfig(item, fill="#E0E0E0")

# 释放按钮
def on_release(items, command, original_color):
    for item in items:
        canvas.itemconfig(item, fill=original_color)
    command()

canvas = tk.Canvas(root, width=500, height=400)
canvas.grid(row=1, column=0, columnspan=4)

# 创建按钮
create_rounded_button(canvas, 10, 10, 90, 60, 20, "清空", clear, '#FFA500')
create_rounded_button(canvas, 100, 10, 180, 60, 20, "归零", guiling, '#FFA500')
create_rounded_button(canvas, 190, 10, 270, 60, 20, "退格", back, '#FFA500')
create_rounded_button(canvas, 280, 10, 360, 60, 20, "+/-", zhengfu, '#FFA500')

create_rounded_button(canvas, 370, 10, 450, 60, 20, "贷款计算器", open_loan_calculator, '#D2691E')
create_rounded_button(canvas, 370, 70, 450, 120, 20, "√", sqrt, '#FFA500')
create_rounded_button(canvas, 370, 130, 450, 180, 20, "1/x", daoshu, '#FFA500')
create_rounded_button(canvas, 370, 190, 450, 240, 20, "%", quyu, '#FFA500')
create_rounded_button(canvas, 370, 250, 450, 300, 20, "=", equal, '#FFA500')

create_rounded_button(canvas, 10, 70, 90, 120, 20, "7", lambda: append_num('7'), '#C0C0C0')
create_rounded_button(canvas, 100, 70, 180, 120, 20, "8", lambda: append_num('8'), '#C0C0C0')
create_rounded_button(canvas, 190, 70, 270, 120, 20, "9", lambda: append_num('9'), '#C0C0C0')
create_rounded_button(canvas, 280, 70, 360, 120, 20, "÷", lambda: yunsuan('÷'), '#FFA500')

create_rounded_button(canvas, 10, 130, 90, 180, 20, "4", lambda: append_num('4'), '#C0C0C0')
create_rounded_button(canvas, 100, 130, 180, 180, 20, "5", lambda: append_num('5'), '#C0C0C0')
create_rounded_button(canvas, 190, 130, 270, 180, 20, "6", lambda: append_num('6'), '#C0C0C0')
create_rounded_button(canvas, 280, 130, 360, 180, 20, "x", lambda: yunsuan('x'), '#FFA500')

create_rounded_button(canvas, 10, 190, 90, 240, 20, "1", lambda: append_num('1'), '#C0C0C0')
create_rounded_button(canvas, 100, 190, 180, 240, 20, "2", lambda: append_num('2'), '#C0C0C0')
create_rounded_button(canvas, 190, 190, 270, 240, 20, "3", lambda: append_num('3'), '#C0C0C0')
create_rounded_button(canvas, 280, 190, 360, 240, 20, "-", lambda: yunsuan('-'), '#FFA500')

create_rounded_button(canvas, 10, 250, 180, 300, 20, "0", lambda: append_num('0'), '#C0C0C0')
create_rounded_button(canvas, 190, 250, 270, 300, 20, ".", lambda: append_num('.'), '#C0C0C0')
create_rounded_button(canvas, 280, 250, 360, 300, 20, "+", lambda: yunsuan('+'), '#FFA500')

root.mainloop()