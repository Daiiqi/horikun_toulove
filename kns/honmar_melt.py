"""
这是用来快速拆刀的脚本
需要在拆刀页面运行
运行前请确定当前库中所有刀没有准备拿去喂乱舞的，
           且没有未满乱舞的孩子在远征
"""
if_stop=False
while not if_stop:
    click(773,554)
    wait(300)
    click(894,550)
    wait(300)
    click(407,374)
    wait(2000)
    if_stop|=check_rgb(403, 149,[54, 88, 166])