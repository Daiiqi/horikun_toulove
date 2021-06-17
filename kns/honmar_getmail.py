# 在本丸界面开启，领取收取箱里的玩意。
if_stop=False
click(971, 129)
while not check_rgb(867, 19,[0, 145, 58]):
    wait(500)
while not if_stop:
    click(735, 184)
    while not check_rgb(272, 70,[0, 149, 64]):
        wait(500)
    if_stop|=check_rgb(437, 126,[251, 90, 82])
    click(871, 37)
    wait(800)
    if_stop|=check_rgb(265, 139,[0, 146, 60])