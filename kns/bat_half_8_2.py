"""
8-2中途返城。
"""
# 中途回城条件为：在小地图上显示到了回城点
middle=[718, 187, [246, 239, 222]]

"""
gb_life 参数为刀装耐久度的比率。
check_balls 取值一览：
    0——不管刀装咋样，总之进军。gb_life设置为多少都无效。
    1——接管金刀装，掉金蛋时中断脚本，金蛋耐久低于gb_life时回城。银的、绿的不管。
    2——同上，接管金银刀装
    3——同上，金银绿刀装都接管
"""

# 主程序
while(1):
    go_battle_simple(8,2, middle=middle, check_balls=2, gb_life=0.26)
