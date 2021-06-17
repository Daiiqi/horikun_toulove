import win32gui, win32api, win32con
import time, random
import tkinter
import os, sys
import threading, inspect, ctypes

# 包装：pyinstaller -F -w horikun.py

# <editor-fold desc="horikun: 基本的界面及功能">
"""
常量定义
"""

TITLELIST = [": v1.1.5", "：最新版！（大概）", ": Hello World", "：持续更新中",
             "：扫地洗衣", "：偷袭暗杀", "：请问兼桑在这里吗？", "",
             "：自定义标题", "：兼桑————————", "：：：", "：检非违使狩猎中",
             "|ω・`)", "：( ˘ω˘`)", "：要不要剪个头发？", ": kanesan.love",
             "：( ^ ^`)", "：我来咏一句吧？梅（以下略）", "：这力量是铁 这力量是钢",
             "：兼桑兼桑兼桑", "：传说中的胁差", "：例行搜查", "：兄弟的筋肉",
             "：邪道", "：也不要忘了兄弟们哦", " : nuk-iroh", "：内置manbachan", "：内置兄弟", ": https://github.com/Daiiqi/horikun_toulove"]
# 每5min输出的提示
MIN_CHAT = ["又是5分钟。", "嗯，5分钟过去了。还要继续呢！",
            "就以5分钟为一步，慢慢走下去吧！",
            "可能5分钟也算不了什么啦。", "每个5分钟都很重要哦！",
            "按照5分钟-7分钟-5分钟来报时如何？", "休息5分钟似乎也不错！", "大概5分钟过去了呢。"]
# 每次运行中log输出小概率夹杂
ON_CHAT = ["兼桑没有惹出什么问题就好……", "顺便一提，兼桑还精神吗？", "对了，兼桑没有偷懒吧？", "啊，兼桑似乎新咏了一句！",
           "任务的安排也要适度，出现负伤者就不好了。", "就照这个劲头干下去吧！", "要洗的衣服堆起来了……",
           "去二十四节气景趣休息一下如何？", "大广间景趣真是华丽呀……有点不习惯呢！", "接下来要去活动吗？",
           "挖山……真是不容易呀！", "就用邪道的方式走下去吧！", "今天的演练有参加吗？", "今天也要找检非吗？",
           "要不要去函馆转换下心情？", "兼桑……嘿嘿。"]
# 选图时的聊天
BATTLE_CHAT = [["是老地方呢，……走吧，去那个战场。", "这个地方……真是怀念呢！", "收集立绘吗？不要太过火哦。", "这里，资源并没有很多呢。"],
               ["Boss点，这次要不要去呢……", "要小心敌太刀哦。", "要小心敌大太刀哦。", "回收依赖札就交给我吧！"],
               ["是关原呢，亲眼看到那场战役！", "玉钢和依赖札，一定带回来！", "木炭和玉钢，捡哪个好些呢？", "织田大人的安土，有缘的刀很多呢！"],
               ["就去捡些依赖札吧！", "是要回收砥石吗？", "了解。是要去收集什么资源呢？", "是冷却材？还是三日月大人呢？"],
               ["为了小乌丸大人，一起加油吧！", "虽然木炭很多，但是敌远程……", "不要午，不要午……", "厚樫山……没什么能说的了呢。"],
               ["京都的市中，努力不要迷路吧！", "在三条大桥上开辟出道路吧！", "好啦……公务搜查！", "一定要……守护那些人们的历史！"],
               ["希望能不要迷路直驱Boss点呢。", "能无伤突破就好了！", "但愿能尽可能减轻损伤……", "编成合适，这里会成为最简单的地图呢！"],
               ["就用远程来攻克这里吧！", "是要提高练度吗？要小心负伤哦！", "", ""]]
# 结束脚本时特殊对话
# 从1个开始，根据输出过的5min log数量决定特殊对话。计数最多50。
min_count = 0
END_CHAT_0 = ["下一个！", "接下来要做什么呢？", "继续下一环节吧！"]
END_CHAT_1 = ["主人也稍作整顿如何？", "稍做整顿，为下个任务打起精神！"]
END_CHAT_2 = ["大家辛苦了！", "长时间出勤辛苦了！"]
DIRECTORY = './kns/'
FOLD = '.py'
t1 = threading.Thread()
t2 = threading.Thread()
# ITSNAME = "计算器"
# ITSNAME="ToukenBrowser"
ITSNAME = "ToukenBrowserChromeWindow"
hwnd = 0
hwndDCf = 0

on_run = False

"""
窗体定义
"""
root = tkinter.Tk()
root.title("hori-kun" + random.choice(TITLELIST))
root.geometry("800x600")
root.configure(bg='#2A3260')
root.resizable(width=False, height=False)

"""
模块2：log
"""
scrl2 = tkinter.Scrollbar(root)
scrl2.place(x=10, y=405, width=635, height=185)

text2 = tkinter.Text(root, bg='white', fg='dimgray', font=("等线", 14), yscrollcommand=scrl2.set)
text2.place(x=10, y=405, width=615, height=185)


def log(result):
    text2.insert(tkinter.END,
                 # time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                 time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))
                 + "   " + result + '\n')
    text2.see(tkinter.END)


log("本程序不为使用脚本所造成的损失承担任何责任")
log("Kuni-kun 1.1.0    暂不支持在程序内编辑脚本")

scrl2['command'] = text2.yview

"""
模块1：选择子文件
"""
if not os.path.exists(DIRECTORY):
    win32api.MessageBox(0, DIRECTORY + "目录缺失，请重新下载哦", "没有找到兼桑", win32con.MB_ICONWARNING)
    sys.exit()

file_name = [os.path.splitext(name)[0] for name in os.listdir(DIRECTORY) if name.endswith(FOLD)]
scrl1 = tkinter.Scrollbar(root)
scrl1.place(x=10, y=10, width=185, height=385)  #

list1 = tkinter.Listbox(root, bg='deepskyblue', fg='black', font=("等线", 16), selectmode=tkinter.BROWSE,
                        yscrollcommand=scrl1.set)
list1.place(x=10, y=10, width=165, height=385)
for item in file_name:
    list1.insert(tkinter.END, item)
scrl1['command'] = list1.yview


def indexstr():
    indexs = list1.curselection()
    if len(indexs) == 0:
        index = 0
    else:
        index = int(indexs[0])
    return DIRECTORY + file_name[index] + FOLD


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


# left, top, right, bottom = win32gui.GetWindowRect(hwnd)

def make_position(cx, cy):
    # 模拟鼠标指针 传送到指定坐标
    return win32api.MAKELONG(cx, cy)


def click_down(cx, cy):
    win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, make_position(cx, cy))  # 模拟鼠标按下
    time.sleep(1e-2)


def click_up(cx, cy):
    win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, make_position(cx, cy))  # 模拟鼠标弹起
    time.sleep(1e-2)


def click(cx, cy):
    click_down(cx, cy)
    click_up(cx, cy)


def wait(t):
    time.sleep(t / 1000)


# win32gui.SetForegroundWindow(hwnd)  # 这句可以把窗口拉到最前面来


def get_RGB(x, y):
    rgba = win32gui.GetPixel(hwndDCf, x, y)
    r = rgba & 255
    g = (rgba >> 8) & 255
    b = (rgba >> 16) & 255
    # rgb = str(r) + ',' + str(g) + ',' + str(b)
    rgb = [r, g, b]
    return rgb


def check_rgb(x, y, rgb2):
    rgb1 = get_RGB(x, y)
    if_rgb = True
    for i in range(3):
        if_rgb &= rgb1[i] == rgb2[i]
    return if_rgb


def check_rgb_rough(x, y, rgb2, err):
    rgb1 = get_RGB(x, y)
    if_rgb = True
    for i in range(3):
        if_rgb &= rgb1[i] - err <= rgb2[i] <= rgb1[i] + err
    return if_rgb


"""
模块3：显示子文件代码
"""
scrl3 = tkinter.Scrollbar(root)
scrl3.place(x=205, y=10, width=585, height=385)


def disp_text(e=None):
    global on_run
    if not on_run:
        with open(indexstr(), 'r', encoding='utf-8') as f:
            content = f.read()
        text3.configure(state='normal')
        text3.delete(0.0, tkinter.END)
        text3.insert(tkinter.INSERT, content)
        text3.configure(state='disabled')


list1.bind('<<ListboxSelect>>', disp_text)

text3 = tkinter.Text(root, bg='white', fg='dimgray', font=("等线", 14), yscrollcommand=scrl3.set)
text3.place(x=205, y=10, width=565, height=385)

text3.insert(tkinter.END, "Hello world!")

scrl3['command'] = text3.yview
disp_text()

"""
模块4：开始/停止按键
"""


def _async_raise(tid, exctype):
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


def endscript(errmsg='None'):
    global t1
    global t2
    global on_run
    on_run = False
    stop_thread(t2)
    log("结束运行。" + choose_end_chat(min_count))
    button4.configure(text="执行\n脚本")
    if not errmsg == 'None':
        # 在这里添加新的异常结束情况弹窗
        if errmsg == 'gb':
            win32api.MessageBox(0, "队内男士的特上刀装损坏了", "金蛋掉了！", win32con.MB_ICONWARNING)
        elif errmsg.find('inj') >= 0:
            if errmsg == 'inj0':
                win32api.MessageBox(0, "出现重伤了", "负伤了！", win32con.MB_ICONWARNING)
            elif errmsg == 'inj1':
                win32api.MessageBox(0, "出现中伤以上伤员了", "负伤了！", win32con.MB_ICONWARNING)
            else:
                win32api.MessageBox(0, "出现轻伤以上伤员了", "负伤了！", win32con.MB_ICONWARNING)
        elif errmsg == 'lim':
            win32api.MessageBox(0, "出阵结束", "结束啦！", win32con.MB_ICONASTERISK)
        else:
            win32api.MessageBox(0, "未定义的结束情况", "怎么回事？", win32con.MB_ICONHAND)
    disp_text()
    stop_thread(t1)


def on_button():
    global on_run
    global min_count
    global t1
    global t2
    if on_run:
        endscript()
    else:
        on_run = True
        t1 = threading.Thread(target=go_run)
        t1.setDaemon(True)
        t1.start()
        t2 = threading.Thread(target=log_rep)
        t2.setDaemon(True)
        t2.start()
        button4.configure(text="停止\n脚本")
        log("开始运行。")
        min_count = 0


def go_run():
    global min_count
    init_params()
    gethwnd()
    try:
        exec(open(indexstr(), encoding='utf-8').read())
    except(Exception, ArithmeticError, IOError, OSError, WindowsError, RuntimeError):
        win32api.MessageBox(0, "脚本代码错误，请再编辑", "出错了！", win32con.MB_ICONWARNING)
        root.destroy()
        win32gui.ReleaseDC(hwnd, hwndDCf)
        sys.exit()
    endscript()


def log_rep():
    while 1:
        time.sleep(300)
        if random.randint(0, 9) < 7:
            log(MIN_CHAT[-1])
        elif random.randint(0, 3):
            log(random.choice(MIN_CHAT[0:-1]))
        else:
            log(random.choice(ON_CHAT))
        global min_count
        if min_count <= 50:
            min_count += 1


def choose_end_chat(count):
    if count == 0:
        return ""
    elif count < 10:
        return random.choice(END_CHAT_0)
    elif count < 40:
        return random.choice(END_CHAT_1)
    else:
        return random.choice(END_CHAT_2)


button4 = tkinter.Button(root, bg='maroon', fg='white', activebackground='crimson',
                         font=("华文行楷", 40), text="执行\n脚本", command=on_button)
button4.place(x=655, y=405, width=135, height=185)
# </editor-fold>

"""
暴力引入实用函数库manbachan
"""

# <editor-fold desc="manbachan: 用来给horikun运行时提供支持的函数库。">
# ---------------------------通用-----------------------------------------------
last_map = False  # 出阵界面默认的出阵图，是否已经固定为上次出阵时的目的地（已不用选择时代）
checked_balls = False  # 是否已经获取了一遍金蛋位置
battles = 0  # 已经出阵过的次数
if_gold_tama = []  # 这个位置上是否是金刀装


def init_params():
    """
    每次按红色按钮启动脚本时，对global变量进行初始化
    """
    global last_map
    global checked_balls
    global battles
    global if_gold_tama
    last_map = False
    checked_balls = False
    battles = 0
    for i in range(6):
        if_gold_tama.append([False, False, False])


def if_in_home():
    # 当前是否在本丸
    return (check_rgb(45, 47, [4, 124, 58]) and
            check_rgb(69, 567, [234, 227, 175]) and
            check_rgb(584, 43, [162, 27, 36]))


def if_in_battle_select():
    # 当前是否在选图界面（普图、活动图皆有可能）
    return (check_rgb(48, 192, [172, 20, 20]) and
            check_rgb(273, 91, [238, 221, 187]) and
            check_rgb(677, 103, [228, 224, 194]))


def if_in_group_select():
    # 当前是否在选择部队界面
    return (check_rgb(827, 124, [120, 214, 216]) and
            check_rgb(28, 241, [98, 11, 11]) and
            check_rgb(651, 160, [0, 53, 134]))


def if_in_formation_select():
    # 当前是否在选择队形界面
    return (check_rgb(175, 70, [198, 23, 23]) and
            check_rgb(233, 213, [80, 179, 14]) and
            check_rgb(549, 391, [192, 100, 54]))


def if_in_battle_count():
    # 当前是否在战斗结束后结算界面
    return (check_rgb(30, 95, [33, 200, 25]) and
            check_rgb(553, 30, [126, 4, 8]) and
            check_rgb(64, 143, [65, 7, 17]))


def if_in_next_point():
    # 当前是否在可以进军的界面
    return (check_rgb(32, 136, [255, 255, 255]) and
            check_rgb(51, 82, [36, 171, 22]) and
            check_rgb(818, 473, [255, 255, 255]))


def if_drop_gb():
    # 在可以进军的界面，检查是否比起出阵时少了金蛋
    if_dropped_gb = False
    for i in range(6):
        for j in range(3):
            if if_gold_tama[i][j] and (
                    not check_rgb_rough(MARCH_GB_X[j], MARCH_GB_Y[i],
                                        MARCH_GB_RGB, MARCH_GB_ERR)):
                if_dropped_gb = True
    return if_dropped_gb


def if_inj_gb(gb_life=0):
    """
    在可以进军的界面，检查金蛋耐久度是否在允许值以下
    参数：耐久占比到这个数以下时就要回城，0~1的浮点数，0为禁用。
    保守值为0.25几乎不会再掉刀装，
    也可以取0.15，降低掉远程刀装的概率
    """
    if_injed_gb = False
    if gb_life and (gb_life < 1):
        for j in range(3):
            check_x = int(gb_life_X_START[j] + gb_life * (gb_life_X_END[j] - gb_life_X_START[j]))
            for i in range(6):
                if if_gold_tama[i][j] and check_rgb(check_x, gb_life_Y[i], gb_life_RGB):
                    if_injed_gb = True
    return if_injed_gb


def if_injure(injury=0):
    """
    在可以进军的界面，检查是否有队员负伤
    参数：
    injury，0-仅重伤，1-中伤以上，2-轻伤以上
    """
    if_injured = False
    for i in range(6):
        for j in range(injury + 1):
            if_injured |= check_rgb_rough(MARCH_INJ_X, MARCH_INJ_Y[i], MARCH_INJ_RGB[j], MARCH_INJ_ERR)
    return if_injured


def enter_battle_face():
    """
    从本丸进入出阵远征演练界面（函数）：
        点击右上调出菜单
        点击出阵按钮
        等待，直到加载出出阵/远征/演练画面
    """
    click(960, 34)
    wait(500)
    click(987, 122)
    wait(800)
    while not if_in_battle_face():
        wait(500)


# 临出阵前检查金刀装位置
ENTER_GB_X = [301, 422, 541]
ENTER_GB_Y = [134, 204, 274, 343, 413, 483]
ENTER_GB_RGB = [255, 215, 94]
ENTER_GB_ERR = 20
# 临进军前检查金刀装位置
MARCH_GB_X = [425, 478, 530]
MARCH_GB_Y = [163, 231, 299, 367, 435, 503]
MARCH_GB_RGB = [255, 210, 86]
MARCH_GB_ERR = 50
# 临进军前检查（金）刀装耐久
gb_life_X_START = [385, 438, 490]
gb_life_X_END = [424, 476, 529]
gb_life_Y = [188, 256, 324, 392, 460, 528]
gb_life_RGB = [102, 54, 3]  # 这个地方因为不是贴图，所以不用设置模糊的ERR
# 临进军前检查负伤情况
MARCH_INJ_X = 208
MARCH_INJ_Y = [137, 205, 273, 341, 409, 477]
MARCH_INJ_RGB = [[239, 0, 0], [255, 119, 0], [239, 204, 0]]  # 重，中，低
MARCH_INJ_ERR = 30  # 10似乎就够了？


def check_gb():
    """
    出门前检查带了多少金蛋
    """
    global if_gold_tama
    # 切换两下，浏览刀装
    click(152, 93)
    wait(500)
    click(152, 93)
    wait(1000)
    # 记录各位置上是否有金蛋
    str_gb = ""
    for i in range(6):
        for j in range(3):
            if_gold_tama[i][j] = check_rgb_rough(ENTER_GB_X[j], ENTER_GB_Y[i], ENTER_GB_RGB, ENTER_GB_ERR)
        str_gb += "\n队员" + str(i + 1) + ": " + str(if_gold_tama[i])
    log("正常刀装情况如下：" + str_gb)


def enter_battle_map():
    """
    决定出阵这个地图（函数）：
        点击右下选队按钮
        等待部队加载
        （跳过刀装/伤势确认）
        记录出阵前有着金刀装的位置
        点击右下出阵按钮
        点击确认“队伍等级超过，是否还要出阵”
    """
    global checked_balls
    click(888, 537)
    wait(500)
    while not if_in_group_select():
        wait(500)
    wait(500)
    if not checked_balls:
        check_gb()
        checked_balls = True
    click(899, 502)  # 点击出阵
    wait(1000)
    click(408, 378)  # 点掉超等级提示
    wait(500)


def enter_battle_map_hanafubuki(change=False):
    """
    刷花时的，决定出阵这个地图。
        点击右下选队按钮
        等待部队加载
        卸刀装，换刀（重点）
        点击右下出阵按钮
        点击确认“队伍等级超过，是否还要出阵”
    """
    click(888, 537)
    wait(500)
    while not if_in_group_select():
        wait(500)
    wait(500)
    # 刷花脚本不检查金刀装。
    if change:
        # 进入队长的刀装界面
        click(658, 145)
        while not check_rgb(571, 31, [124, 81, 44]):
            wait(500)
        # 一键解除刀装
        click(494, 548)
        while not check_rgb(288, 195, [233, 227, 197]):
            wait(500)
        # 随便点外面哪个地方，退出刀装界面
        click(865, 170)
        wait(800)
        # 换人
        click(570, 152)
        while not check_rgb(351, 99, [114, 111, 0]):
            wait(500)
        # 激活filter
        click(176, 556)
        wait(500)
        # 选择“有刀装的”
        click(244, 445)
        wait(500)
        # 应用filter
        click(785, 451)
        wait(800)
        # 选择第一个
        if check_rgb(436, 119, [136, 128, 31]):
            endscript('lim')
        else:
            click(939, 141)
            while not check_rgb(367, 102, [233, 222, 187]):
                wait(500)
    wait(500)
    click(899, 502)  # 点击出阵
    wait(1000)
    click(408, 378)  # 点掉超等级提示
    wait(500)


# 预定义 各阵型对应的判断有利/不利位置
FORMATIONS = [[178, 183],  # 各个阵型对应的坐标
              [428, 183],
              [676, 183],
              [178, 357],
              [428, 357],
              [676, 357]]
FORMATION_GOOD = [219, 2, 2]  # 注意当k为有利阵型时，敌阵型是k+1
FORMATION_BAD = [2, 119, 218]  # 这个大概用不到


# 阵型编号 0~5
def manual_formation(form_blind, if_enemy=None, then_mine=None):
    """
    手动选择阵型（函数：盲选的阵型，特殊情况的敌阵型、我阵型）
        # 提供特殊情况下的手选
        若优势阵型代表的是特殊情况
            则选择特殊答案
        若其余五个阵型中某一个阵型为优势
            则选择那个优势的
        其他（侦察失败）
            则选择盲选的
    """
    enemy = form_blind + 1
    for i in range(6):
        if check_rgb(FORMATIONS[i][0], FORMATIONS[i][1], FORMATION_GOOD):
            enemy = i + 1
            break
    if enemy >= 6:
        enemy -= 6
    if enemy == if_enemy or enemy - 6 == if_enemy:
        click(FORMATIONS[then_mine][0], FORMATIONS[then_mine][1])
    else:
        click(FORMATIONS[enemy - 1][0], FORMATIONS[enemy - 1][1])


# -------------------------一般出阵---------------------------------------------


def if_in_battle_face():
    # 当前是否在一般出阵界面
    return (check_rgb(172, 96, [183, 227, 254]) and
            check_rgb(425, 69, [61, 115, 210]) and
            check_rgb(166, 546, [142, 186, 66]))


def if_in_battle_normal():
    # if_in_battle_select的前提下，当前是否在普图界面
    return ((check_rgb(369, 126, [140, 0, 0]) or check_rgb(306, 128, [140, 0, 0])) and
            check_rgb(996, 533, [0, 52, 134]) and
            check_rgb(244, 276, [190, 0, 0]))


def if_in_KBC():
    # 当前是否遭遇检非
    return (check_rgb(320, 109, [8, 254, 236]) and
            check_rgb(329, 305, [24, 96, 102]) and
            check_rgb(767, 107, [4, 44, 255]))


def enter_battle_select():
    """
    从本丸进入普图界面（函数）：
        从本丸进入选择出阵界面（函数）
        选择“出阵”
        等待，直到加载出选图画面
        如果跑到活动图去了，往前一级回到普图选图界面
    """
    enter_battle_face()
    click(546, 225)
    wait(500)
    while not if_in_battle_select():
        wait(500)
    if not if_in_battle_normal():
        click(137, 93)
        wait(500)


def which_map():
    """
    在普图选图界面，判断现在选中的是哪个时代
    每个图的判据都是独特的，顺序可根据需求重排
    1: check_rgb(597, 510,[84,83,69])
    2: check_rgb(525, 553,[0,0,0])
    3: check_rgb(688, 534,[10,10,8])
    4: check_rgb(482, 497,[104,101,85])
    5: check_rgb(179, 568,[32,31,26])
    6: check_rgb(780, 525,[0,0,0])
    7: check_rgb(702, 500,[0,0,0])
    8: check_rgb(544, 561,[0,0,0])
    """
    if check_rgb(524, 569, [43, 40, 37]):
        current_map = 5
    elif check_rgb(558, 560, [0, 0, 0]):
        current_map = 8
    elif check_rgb(597, 508, [1, 1, 1]):
        current_map = 1
    elif check_rgb(135, 533, [84, 83, 74]):
        current_map = 4
    elif check_rgb(434, 509, [16, 15, 12]):
        current_map = 3
    elif check_rgb(526, 549, [2, 2, 2]):
        current_map = 2
    elif check_rgb(631, 545, [0, 0, 0]):
        current_map = 7
    else:  # (780, 524 ,[0, 0, 0])
        current_map = 6
    log("当前光标所指时代为 " + str(current_map) + "图")
    return current_map


# 普图一个时代四个图的选择点
MAP4 = [[673, 342], [905, 349], [663, 445], [880, 443]]


# 是否已在上次出阵时留下选图记录


def map_select(m, n, la_map=False):
    """
    普图选地图（函数：要选择的那个图是m-n）
        若还没定义上次的出阵先：
            判断当前所在大战场是m图（进入判断战场部分）
            若m不对
                点击左右箭头对应次数，让m对上
            （无等待）点击对应的n
    """
    if not la_map:
        delta_map = m - which_map()
        if delta_map >= 0:  # 目标图号>当前所指图号
            for i in range(delta_map):
                if check_rgb(705, 215, [255, 255, 255]):
                    click(705, 215)
                elif check_rgb(990, 215, [255, 255, 255]):
                    click(990, 215)
                wait(500)
        else:
            for i in range(-delta_map):
                click(109, 217)
                wait(500)
    click(MAP4[n - 1][0], MAP4[n - 1][1])
    wait(500)


def go_battle_simple(m, n, middle=None, injury=0, limit=0, gb_life=0):
    """
    从本丸或者战中的任何一个点开始，进入无脑loop的循环
    参数：
    m : 1~8 的整数，出阵的时代
    n : 1~4 的整数，出阵的具体地图
    middle : 形如[x,y,[r,g,b]]的数组, 当满足这个颜色条件的时候，说明该中途回城了
    injure : 0-重，1-中，2-轻的整数，中止脚本所需伤势
    limit : 最大出阵次数，刷花时设成3就行。
    gb_life : 0~1的浮点数，金蛋的耐久度小于这个比率时就该回城了。
    """
    global last_map
    global battles
    if if_in_home():
        # 在本丸内
        if limit and battles >= limit:
            endscript('lim')  # 结束，并告知是因为到达出阵上限退出的
        enter_battle_select()
        map_select(m, n, last_map)
        enter_battle_map()
        battles += 1
        if not last_map:
            log(BATTLE_CHAT[m - 1][n - 1])
            last_map = True
        else:
            log("出阵 × " + str(battles))
    elif if_in_next_point():
        # 到了该进军的时候
        if_mid = False
        if middle:
            if_mid = check_rgb(middle[0], middle[1], middle[2])  # 是否到该回城的预设点
        if_dropped_gb = if_drop_gb()
        if_injed_gb = if_inj_gb(gb_life)
        if_injured = if_injure(injury)
        if if_mid or if_injed_gb or if_dropped_gb or if_injured:  # 到地方了，要回城了
            click(932, 440)
            wait(500)
            click(415, 377)
            # 中途点回城 属正常情况
            # 刀装低耐久度回城 属正常情况
            if if_dropped_gb:  # 掉金蛋必退出
                endscript('gb')  # 结束后告知是因为掉蛋而退出的
            elif if_injured:  # 负伤要看程度
                endscript('inj' + str(injury))
        wait(500)
        click(631, 449)
    else:
        click(631, 157)  # 没啥事的时候点上面，憋点下边，要不然可能误触进军
    wait(1000)


def auto_hanafubuki(limit=3):
    """
    全自动刷花。
    基本结构如上，但有些许的modify。
    """
    global last_map
    global battles
    auto_hanafubuki.change = False
    if if_in_home():
        # 在本丸内
        if battles >= limit:
            auto_hanafubuki.change = True
            battles = 0
        enter_battle_select()
        map_select(1, 1, last_map)
        enter_battle_map_hanafubuki(auto_hanafubuki.change)
        auto_hanafubuki.change = False
        battles += 1
        if not last_map:
            log("去恢复疲劳度吧！")
            last_map = True
        else:
            log("出阵 × " + str(battles))
    else:
        # 刷花时不设置禁止进军的条件。
        click(631, 449)  # 无脑进军
    wait(1000)


# -------------------------通用活动---------------------------------------------


def if_in_campaign_face(campaign_name):
    # if_in_battle_select的前提下，当前是否在某个活动图界面
    ifin = False
    if campaign_name == "hanafuda":
        ifin = (check_rgb(131, 139, [215, 64, 64]) and
                check_rgb(388, 181, [255, 165, 188]) and
                check_rgb(722, 178, [255, 208, 135]))
    return ifin


def enter_campaign_face():
    """
    从本丸进入活动图界面（函数）：
        若左侧活动菜单没调出来
            点击左侧小三角调出活动菜单
        点击活动banner
        等待，直到加载出活动界面
        若有4个地图：
            点击所设定的地图
    """
    click(109, 137)
    wait(500)
    click(109, 137)
    wait(500)
    # wait until hanafuda
    while not if_in_campaign_face("hanafuda"):
        wait(500)
    click(482, 401)
    wait(500)


def enter_campaign_map():
    """
    决定出阵这个活动地图
    """
    enter_battle_map()
    # 这里采取花札的门票位置
    click(504, 454)
    wait(1000)


def fill_ticket():
    """
    如果目前已经1个门票都没了，就回复1。不回复更多的了，我也怕浪费。
    """
    if check_rgb(212, 223, [48, 32, 13]):
        click(651, 213)
        wait(500)
        click(309, 373)
        wait(500)
        click(404, 367)
        wait(500)
        while not check_rgb(509, 369, [209, 0, 88]):
            wait(500)
        click(509, 367)
        wait(500)


# --------------------------大阪城----------------------------------------------

def if_in_next_stage():
    # （大阪城）当前是否在可以进入下一层的界面
    pass


# ---------------------------花札-----------------------------------------------

def hanafuda_if_on_koikoi():
    # 可以agari了
    return (check_rgb(381, 151, [0, 114, 40]) and
            check_rgb(663, 224, [0, 119, 45]) and
            check_rgb(327, 284, [152, 77, 17]))


def hanafuda_if_on_select():
    # 当前在花札内，可以选牌了
    return (check_rgb(264, 25, [155, 153, 135]) and
            check_rgb(935, 455, [134, 0, 0]) and
            check_rgb(942, 196, [85, 76, 41]))


def hanafuda_if_finish():
    # 当前花札已经跑完，该选牌回家了
    return (check_rgb(228, 20, [123, 39, 37]) and
            check_rgb(735, 377, [26, 22, 18]) and
            check_rgb(1011, 77, [197, 163, 114]))


def hanafuda_if_finish_count():
    # 选完牌，结算完奖励，真该回家了
    return (check_rgb(571, 93, [38, 10, 5]) and
            check_rgb(892, 108, [91, 75, 57]) and
            check_rgb(919, 462, [134, 0, 0]))


"""
用来判断各种役的绿边位置。存储位置为该役的[y, x1,x2,...]
    HANAFUDA_KOU =[461, 26,56,86,116,146] # 五光，基础分5
    HANAFUDA_TANN=[530, 225,255,285,315,345,375] # タン，基础分2
    HANAFUDA_TANE=[530, 515,545,575,605,635,665] # タネ，基础分2
    HANAFUDA_KASU=[530, 704,734,764,794,834,854,884,914,944,974,1004] # カス，基础分1
    # 以下特殊组合加分均为2
    HANAFUDA_HANA=[461, 414,444] # 月见酒
    HANAFUDA_TUKI=[461, 484,514] # 花见酒
    HANAFUDA_AKAN=[530, 26,56,86] # 赤短
    HANAFUDA_AOTN=[530, 126,156,186] # 青短
    HANAFUDA_SISI=[530, 415,445,475] # 猪鹿蝶
    # 若在以上组合中取到了末尾的坐标，则直接加分5
常量按照分数区别定义如下:[score, y, [x1,x2,...,xn]]
"""
HANAFUDA_SCORE = [[5, 461, [26, 56, 86, 116, 146]],
                  [2, 530, [225, 255, 285, 315, 345, 375]],
                  [2, 530, [515, 545, 575, 605, 635, 665]],
                  [1, 530, [704, 734, 764, 794, 834, 854, 884, 914, 944, 974, 1004]],
                  [2, 461, [414, 444]],
                  [2, 461, [484, 514]],
                  [2, 530, [26, 56, 86]],
                  [2, 530, [126, 156, 186]],
                  [2, 530, [415, 445, 475]]]
HANAFUDA_GREEN = [102, 242, 47]  # 绿色边的主色，如果取得太靠边就不是这个颜色了


def hanafuda_level():
    """
    光标已经移到花札上时，通过底边栏判断花札选择优先级
    """
    score = 0
    for i in range(len(HANAFUDA_SCORE)):
        if check_rgb_rough(HANAFUDA_SCORE[i][2][len(HANAFUDA_SCORE[i][2]) - 1],
                           HANAFUDA_SCORE[i][1],
                           HANAFUDA_GREEN, 20):
            score += HANAFUDA_SCORE[i][0] + 5
            continue
        for j in reversed(range(len(HANAFUDA_SCORE[i][2]) - 1)):
            if check_rgb_rough(HANAFUDA_SCORE[i][2][j],
                               HANAFUDA_SCORE[i][1],
                               HANAFUDA_GREEN, 20):
                score += HANAFUDA_SCORE[i][0]
                break
    return score


HANAFUDA_X = [312, 436, 542, 656]
HANAFUDA_Y = [200, 410]


def hanafuda_select():
    # 当面前摆着两张或三张花札时，选择一张
    sum_score = [0, 0, 0, 0]
    for i in range(4):
        cx = HANAFUDA_X[i]
        click_down(cx, HANAFUDA_Y[0])  # 假点击。在牌面点击，
        wait(500)
        sum_score[i] = hanafuda_level()  # 趁机用底边绿边算分数，
        wait(500)
        click_up(cx, HANAFUDA_Y[1])  # 在另一个地方抬起，模拟鼠标“移动”
    x = sum_score.index(max(sum_score))  # 选择得分最高的卡，
    click(HANAFUDA_X[x], HANAFUDA_Y[0])  # 点它
    wait(500)
    click(HANAFUDA_X[x], HANAFUDA_Y[0])  # 以防抬起失败，做双击处理


def go_hanafuda_simple():
    """
    从本丸开始，进入loop
    """
    if if_in_home():
        enter_campaign_face()
        fill_ticket()  # 虚拟伤害，保持总有一张门票可以用
        enter_campaign_map()
        # 这里就进入了花札地图。
    elif hanafuda_if_on_koikoi():
        # 如果koikoi就它，如果只有agari就它
        click(552, 208)
        wait(500)
        click(552, 208)
        wait(500)
    elif hanafuda_if_on_select():
        wait(2000)
        hanafuda_select()
        wait(500)
    elif hanafuda_if_finish():
        # 如果一圈跑完了，怎么进行后续操作（直到回到本丸/继续出击）
        # 先选5张牌
        wait(1000)
        for i in range(5):
            click(160 + i * 140, 200)
            wait(500)
        while not hanafuda_if_finish_count():
            click(634, 482)
            wait(800)
        click(919, 450)
        wait(5000)
    else:
        # 无脑点进军
        for i in range(3):
            click(634, 482)
            wait(800)


# ------------------------------------------manbachan 结束------------------------------------------
# </editor-fold>


"""
开始主循环
"""
root.mainloop()
