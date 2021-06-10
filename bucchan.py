import win32gui, win32api, win32con
import time, random
import tkinter

"""
点击ctrl记录像素颜色
"""
TITLELIST = ["", " : Hello kyoudai"]
ITSNAME = "ToukenBrowserChromeWindow"
hwnd = 0
hwndDCf = 0
curind = 0
# 包装：pyinstaller -F -w bucchan.py
"""
窗体定义
"""
root = tkinter.Tk()
root.title("bucchan" + random.choice(TITLELIST))
root.geometry("800x600")
root.configure(bg='#FFFFFF')
root.resizable(width=False, height=False)
"""
模块2：log
"""
scrl2 = tkinter.Scrollbar(root)
scrl2.place(x=50, y=500, width=700, height=100)

text2 = tkinter.Text(root, bg='white', fg='dimgray', font=("等线", 14), yscrollcommand=scrl2.set)
text2.place(x=50, y=500, width=680, height=100)


def log(result):
    text2.insert(tkinter.END,
                 # time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                 time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))
                 + "   " + result + '\n')
    text2.see(tkinter.END)


log("Bucchan 0.3.3    激活该窗口时，按左shift记录鼠标所在像素颜色")

scrl2['command'] = text2.yview

"""
核心功能
"""


def gethwnd():
    global hwnd
    global hwndDCf
    win32gui.ReleaseDC(hwnd, hwndDCf)
    hwnd = win32gui.FindWindow(None, ITSNAME)
    while hwnd == 0:
        log("等待获取%s窗口 ..." % ITSNAME)
        time.sleep(3)
        hwnd = win32gui.FindWindow(None, ITSNAME)
    hwndDCf = win32gui.GetWindowDC(hwnd)
    log("已获取窗口，句柄为%d" % hwnd)


def get_RGB(x, y):
    rgba = win32gui.GetPixel(hwndDCf, x, y)
    r = rgba & 255
    g = (rgba >> 8) & 255
    b = (rgba >> 16) & 255
    # rgb = str(r) + ',' + str(g) + ',' + str(b)
    rgb = [r, g, b]
    return rgb


def RGB_to_Hex(rgb):  # 输入形如[197,224,64]，输出'#C5E040'.这个函数在程序3里才用到。
    color = '#'
    for i in rgb:
        num = int(i)
        # 将R、G、B分别转化为16进制拼接转换并大写  hex() 函数用于将10进制整数转换成16进制，以字符串形式表示
        color += str(hex(num))[-2:].replace('x', '0').upper()
    return color


"""
模块1：显色框
"""
labelxy = []
xys = []
for i in range(8):
    xys.append(tkinter.StringVar())
    xys[i].set("(x, y)")
for i in range(4):
    labelxy.append(tkinter.Label(root, textvariable=xys[i], bg='white', fg='black',
                                 width=20, height=3, font=("等线", 14)))
    labelxy[i].place(x=i * 200, y=130)
for i in range(4):
    labelxy.append(tkinter.Label(root, textvariable=xys[4 + i], bg='white', fg='black',
                                 width=20, height=3, font=("等线", 14)))
    labelxy[4 + i].place(x=i * 200, y=380)

labelrgb = []
rgbs = []
for i in range(8):
    rgbs.append(tkinter.StringVar())
    rgbs[i].set("(r, g, b)")
for i in range(4):
    labelrgb.append(tkinter.Label(root, textvariable=rgbs[i], bg='white', fg='black',
                                  width=20, height=3, font=("等线", 14)))
    labelrgb[i].place(x=i * 200, y=170)
for i in range(4):
    labelrgb.append(tkinter.Label(root, textvariable=rgbs[4 + i], bg='white', fg='black',
                                  width=20, height=3, font=("等线", 14)))
    labelrgb[4 + i].place(x=i * 200, y=420)

labelcolor = []
for i in range(4):
    labelcolor.append(tkinter.Label(root, bg='white', width=20, height=7, font=("等线", 14)))
    labelcolor[i].place(x=i * 200, y=0)
for i in range(4):
    labelcolor.append(tkinter.Label(root, bg='white', width=20, height=7, font=("等线", 14)))
    labelcolor[4 + i].place(x=i * 200, y=250)


def getcolor(e=None):
    global curind
    global hwnd
    global hwndDCf
    if not (hwnd or hwndDCf):
        gethwnd()
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    (x, y) = win32gui.ScreenToClient(hwnd, win32api.GetCursorPos())
    if (0 < x <= (right - left)) & (0 < y <= (bottom - top)):
        rgb = get_RGB(x, y)
        strxy = str(x) + ', ' + str(y)
        strrgb = str(rgb[0]) + ', ' + str(rgb[1]) + ', ' + str(rgb[2])
        xys[curind].set(strxy)
        rgbs[curind].set(strrgb)
        labelcolor[curind].configure(bg=RGB_to_Hex(rgb))
        log("获取第" + str(curind + 1) + "点成功，(x, y) = (" + strxy + "),   (r, g, b) = (" + strrgb + ")")
        curind += 1
        if curind >= 8:
            curind = 0
    else:
        log("所点击位置不在窗口范围内")


root.bind("<Shift_L>", getcolor)

root.mainloop()
