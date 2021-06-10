"""
8-2中途返城。是一个添了点东西的用户脚本。
"""
def go_battle_82_mid():
    """
    从本丸或者战中的任何一个点开始，进入无脑loop的循环
    """
    global last_map
    if if_in_home():
        enter_battle_select()   # 从本丸进入选地图的画面
        map_select(8, 2, last_map)  # 选择8-2
        enter_battle_map()      # 进图
        if not last_map:
            log(BATTLE_CHAT[8-1][2-1])      # 输出个8-2专用log
            last_map = True
    else:   # 不在本丸，在战场里
        if_82_march = check_rgb(324, 54 , [56 , 120, 27 ]) and check_rgb(946, 83 , [107, 132, 107]) and check_rgb(936, 415, [255, 255, 255])
        if if_82_march:         # 到了该进军的时候
            if_82_mid = check_rgb(718, 187, [246, 239, 222]) and check_rgb(718, 179, [136, 120, 112])
            if_drop_gb = False
            for i in range(6):
                for j in range(3):
                    if if_gold_tama[i][j] and (not check_rgb_rough(MARCH_GB_X[j],MARCH_GB_Y[i],MARCH_GB_RGB,MARCH_GB_ERR)):
                        if_drop_gb = True
            if if_82_mid or if_drop_gb:       # 到地方了，要回城了
                click(932, 440)
                wait(500)
                click(415, 377)
                if if_drop_gb:
                    win32api.MessageBox(0, "队内第 "+str(i+1)+" 位男士的第 "+str(j+1)+" 个刀装损坏了", "掉蛋了！", win32con.MB_ICONWARNING)
                    endscript()
            else:
                click(631, 449)
        else:
            click(631, 449)
    wait(1000)

# 主程序    
while(1):
    go_battle_82_mid()
    