"""
无脑出阵5-4。可以用记事本打开这里，修改参数中的前两个数字。
已有功能：
    掉刀装中断（设置check_balls为1、2、3，分别对应金、金银、金银绿刀装的检查）
    检查刀装耐久（在上者起效的前提下，设gb_life为 0~1 的小数）
    重伤中断（想要 中伤/轻伤 回城，可以把injury的 0 改成 1 或 2）
    定义出阵次数（把limit取值设为1以上的整数时起效）
"""
while(1):
    go_battle_simple(5, 4, middle=None, injury=0, limit=0, check_balls=3, gb_life=0)