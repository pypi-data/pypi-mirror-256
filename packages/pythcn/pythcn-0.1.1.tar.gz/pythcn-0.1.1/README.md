# Pythcn

## 安装（Intall）

```any
pip install pythcn
```

## 例子（Example）

```python
import pycn
@pycn_run
def pycn():
    """
    甲=整数（输入（））
    乙=整数（输入（））
    输出（甲+乙）
    """
```

## 关键词（Keyword）

让我们来看看关键词翻译成中文会是什么了？

```python
#内置函数

# 绝对值（。。。） => abs(...) | 函数-Function
# 全部（。。。） => all(...) | 函数-Function
# 任意（。。。） => any(...) | 函数-Function
# 代码（。。。） => ascii(...) | 函数-Function
# 二进制（。。。） => bin(...) | 函数-Function
# 布尔值（。。。） => bool(...) | 函数-Function
# 字节数组（。。。） => bytearray(...) | 函数-Function
# 字节（。。。） => bytes(...) | 函数-Function
# 可调用（。。。） => callable(...) | 函数-Function
# 字符（。。。） => chr(...) | 函数-Function
# 类方法（。。。） => classmethod(...) | 函数-Function
# 编译（。。。） => compile(...) | 函数-Function
# 复数（。。。） => complex(...) | 函数-Function
# 删除属性（。。。） => delattr(...) | 函数-Function
# 字典（。。。） => dict(...) | 函数-Function
# 目录（。。。） => dir(...) | 函数-Function
# 带余除法（。。。） => divmod(...) | 函数-Function
# 枚举（。。。） => enumerate(...) | 函数-Function
# 解析（。。。） => eval(...) | 函数-Function
# 执行（。。。） => exec(...) | 函数-Function
# 过滤（。。。） => filter(...) | 函数-Function
# 浮点数（。。。） => float(...) | 函数-Function
# 格式化（。。。） => format(...) | 函数-Function
# 冻结集合（。。。） => frozenset(...) | 函数-Function
# 获取属性（。。。） => getattr(...) | 函数-Function
# 全局变量（。。。） => globals(...) | 函数-Function
# 包含属性（。。。） => hasattr(...) | 函数-Function
# 哈希值（。。。） => hash(...) | 函数-Function
# 帮助（。。。） => help(...) | 函数-Function
# 十六进制（。。。） => hex(...) | 函数-Function
# 地址（。。。） => id(...) | 函数-Function
# 输入（。。。） => input(...) | 函数-Function
# 整数（。。。） => int(...) | 函数-Function
# 是否为类（。。。） => isinstance(...) | 函数-Function
# 是否子类（。。。） => issubclass(...) | 函数-Function
# 迭代（。。。） => iter(...) | 函数-Function
# 长度（。。。） => len(...) | 函数-Function
# 列表（。。。） => list(...) | 函数-Function
# 局部变量（。。。） => locals(...) | 函数-Function
# 映射（。。。） => map(...) | 函数-Function
# 最大值（。。。） => max(...) | 函数-Function
# 最小值（。。。） => min(...) | 函数-Function
# 内存查看（。。。） => memoryview(...) | 函数-Function
# 下一个（。。。） => next(...) | 函数-Function
# 对象（。。。） => object(...) | 函数-Function
# 打开（。。。） => open(...) | 函数-Function
# 八进制（。。。） => oct(...) | 函数-Function
# 顺序（。。。） => ord(...) | 函数-Function
# 幂（。。。） => pow(...) | 函数-Function
# 输出（。。。） => print(...) | 函数-Function
# 属性（。。。） => property(...) | 函数-Function
# 范围（。。。） => range(...) | 函数-Function
# 解释（。。。） => repr(...) | 函数-Function
# 反转（。。。） => reversed(...) | 函数-Function
# 四舍五入（。。。） => round(...) | 函数-Function
# 集合（。。。） => set(...) | 函数-Function
# 设置属性（。。。） => setattr(...) | 函数-Function
# 切片（。。。） => slice(...) | 函数-Function
# 排序（。。。） => sorted(...) | 函数-Function
# 静态方法（。。。） => staticmethod(...) | 函数-Function
# 字符串（。。。） => str(...) | 函数-Function
# 求和（。。。） => sum(...) | 函数-Function
# 继承（。。。） => super(...) | 函数-Function
# 元组（。。。） => tuple(...) | 函数-Function
# 类型（。。。） => type(...) | 函数-Function
# 变量（。。。） => vars(...) | 函数-Function
# 打包（。。。） => zip(...) | 函数-Function
# 导库（。。。） => __import__(...) | 函数-Function

# 关键词
# 导入 。。。 => import ... | 关键词-Keyword
# 从 。。。 导入 。。。 => from ... import ...
# 作为 。。。 => as ...
# 如果 。。。 => if ...
# 否则如果 。。。 => elif ...
# 否则 。。。 => else ...
# 匹配 。。。 => match ...
# 情况 。。。 => case ...
# 当 。。。 => while ...
# 给 。。。 => for ...
# 用 。。。 => with ...
# 举起 。。。=> raise ...
# 尝试 => try
# 除了 。。。 => except ...
# 最后 => finally
# 断言 。。。 => assert ...
# 全局 。。。 => global ...
# 定义 。。。 => def ...
# 匿名函数 。。。 => lambda ...
# 返回 。。。 => rteurn ...
# 生成 。。。 => yield ...
# 删除 。。。 => del ...
# 继续 => continue
# 通过 => pass
# 与 => and
# 或 => or
# 非 => not
# 在 => in
# 不在 => not in
# 是 => is
# 不是 => is not
# 真 => True
# 假 => False
# 空 => None
# 自己 => self
# 原类 => cls

#类的魔法方法

# -初始化-（。。。） => __init__(...) | 方法-Method
# -创建-（。。。） => __new__(...) | 方法-Method
# -删除-（。。。） => __del__(...) | 方法-Method
# -调用-（。。。） => __call__(...) | 方法-Method
# -获取属性-（。。。） => __getattr__(...) | 方法-Method
# -设置属性-（。。。） => __setattr__(...) | 方法-Method
# -删除属性-（。。。） => __delattr__(...) | 方法-Method
# -目录-（。。。） => __dir__(...) | 方法-Method
# -长度-（。。。） => __len__(...) | 方法-Method
# -加法-（。。。） => __add__(...) | 方法-Method
# -减法-（。。。） => __sub__(...) | 方法-Method
# -乘法-（。。。） => __mul__(...) | 方法-Method
# -除法-（。。。） => __truediv__(...) | 方法-Method
# -整除-（。。。） => __floordiv__(...) | 方法-Method
# -取模-（。。。） => __mod__(...) | 方法-Method
# -带余除法-（。。。） => __divmod__(...) | 方法-Method
# -求幂-（。。。） => __pow__(...) | 方法-Method
# -小于-（。。。） => __lt__(...) | 方法-Method
# -大于-（。。。） => __gt__(...) | 方法-Method
# -等于-（。。。） => __eq__(...) | 方法-Method
# -小于等于-（。。。） => __le__(...) | 方法-Method
# -大于等于-（。。。） => __ge__(...) | 方法-Method
# -不等于-（。。。） => __ne__(...) | 方法-Method
# -位与-（。。。） => __and__(...) | 方法-Method
# -位或-（。。。） => __or__(...) | 方法-Method
# -位异或-（。。。） => __xor__(...) | 方法-Method
# -左移-（。。。） => __lshift__(...) | 方法-Method
# -右移-（。。。） => __rshift__(...) | 方法-Method
# -反加法-（。。。） => __radd__(...) | 方法-Method
# -反减法-（。。。） => __rsub__(...) | 方法-Method
# -反乘法-（。。。） => __rmul__(...) | 方法-Method
# -反除法-（。。。） => __rtruediv__(...) | 方法-Method
# -反整除-（。。。） => __rfloordiv__(...) | 方法-Method
# -反取模-（。。。） => __rmod__(...) | 方法-Method
# -反求幂-（。。。） => __rpow__(...) | 方法-Method
# -反位与-（。。。） => __rand__(...) | 方法-Method
# -反位或-（。。。） => __ror__(...) | 方法-Method
# -反位异或-（。。。） => __rxor__(...) | 方法-Method
# -反左移-（。。。） => __rlshift__(...) | 方法-Method
# -反右移-（。。。） => __rrshift__(...) | 方法-Method
# -赋值加法-（。。。） => __iadd__(...) | 方法-Method
# -赋值减法-（。。。） => __isub__(...) | 方法-Method
# -赋值乘法-（。。。） => __imul__(...) | 方法-Method
# -赋值除法-（。。。） => __itruediv__(...) | 方法-Method
# -赋值整除-（。。。） => __ifloordiv__(...) | 方法-Method
# -赋值取模-（。。。） => __imod__(...) | 方法-Method
# -赋值求幂-（。。。） => __ipow__(...) | 方法-Method
# -赋值位与-（。。。） => __iand__(...) | 方法-Method
# -赋值位或-（。。。） => __ior__(...) | 方法-Method
# -赋值位异或-（。。。） => __ixor__(...) | 方法-Method
# -赋值左移-（。。。） => __ilshift__(...) | 方法-Method
# -赋值右移-（。。。） => __irshift__(...) | 方法-Method
# -正-（。。。） => __pos__(...) | 方法-Method
# -负-（。。。） => __neg__(...) | 方法-Method
# -绝对值-（。。。） => __abs__(...) | 方法-Method
# -取反-（。。。） => __invert__(...) | 方法-Method
# -向上取整-（。。。） => __ceil__(...) | 方法-Method
# -向下取整-（。。。） => __floor__(...) | 方法-Method
# -四舍五入-（。。。） => __round__(...) | 方法-Method
# -存在-（。。。） => __contains__(...) | 方法-Method
# -表示-（。。。） => __repr__(...) | 方法-Method
# -格式化-（。。。） => __format__(...) | 方法-Method
# -整数-（。。。） => __int__(...) | 方法-Method
# -浮点数-（。。。） => __float__(...) | 方法-Method
# -复数-（。。。） => __complex__(...) | 方法-Method
# -布尔值-（。。。） => __bool__(...) | 方法-Method
# -字符串-（。。。） => __str__(...) | 方法-Method
# -列表-（。。。） => __list__(...) | 方法-Method
# -字典-（。。。） => __dict__(...) | 方法-Method
# -进入-（。。。） => __enter__(...) | 方法-Method
# -退出-（。。。） => __exit__(...) | 方法-Method
# -迭代-（。。。） => __iter__(...) | 方法-Method
# -下一个-（。。。） => __next__(...) | 方法-Method

#随机库函数

# 种子（。。。） => seed(...) | 函数-Function
# 随机数（。。。） => random(...) | 函数-Function
# 随机整数（。。。） => randint(...) | 函数-Function
# 随机小数（。。。） => uniform(...) | 函数-Function
# 随机范围（。。。） => randrange(...) | 函数-Function
# 随机字节（。。。） => randbytes(...) | 函数-Function
# 选择（。。。） => choice(...) | 函数-Function
# 打乱顺序（。。。） => shuffle(...) | 函数-Function

#数学库函数&常量

# 向上取整（。。。） => ceil(...) | 函数-Function
# 向下取整（。。。） => floor(...) | 函数-Function
# 以e为底的对数（。。。） => log(...) | 函数-Function
# 以2为底的对数（。。。） => log2(...) | 函数-Function
# 以10为底的对数（。。。） => log10(...) | 函数-Function
# 平方根（。。。） => sqrt(...) | 函数-Function
# e的次幂（。。。） => exp(...) | 函数-Function
# 最大公因数（。。。） => gcd(...) | 函数-Function
# 最大公约数（。。。） => gcd(...) | 函数-Function
# 正弦（。。。） => sin(...) | 函数-Function
# 余弦（。。。） => cos(...) | 函数-Function
# 正切（。。。） => tan(...) | 函数-Function
# 反正弦（。。。） => asin(...) | 函数-Function
# 反余弦（。。。） => acos(...) | 函数-Function
# 反正切（。。。） => atan(...) | 函数-Function
# 双曲正弦（。。。） => sinh(...) | 函数-Function
# 双曲余弦（。。。） => cosh(...) | 函数-Function
# 双曲正切（。。。） => tanh(...) | 函数-Function
# 反双曲正弦（。。。） => asinh(...) | 函数-Function
# 反双曲余弦（。。。） => acosh(...) | 函数-Function
# 反双曲正切（。。。） => atanh(...) | 函数-Function
# 圆周率 => pi | 常量-Constant
# 自然对数 => e | 常量-Constant
# 无穷大 => inf | 常量-Constant
# 非数字 => nan | 常量-Constant

#时间库函数

# 时间戳（。。。） => time(...) | 函数-Function
# 睡眠（。。。） => sleep(...) | 函数-Function
# 解析时间（。。。） => strptime(...) | 函数-Function
# 格式化时间（。。。） => strftime(...) | 函数-Function
# 世界时间（。。。） => gmtime(...) | 函数-Function
# 当地时间（。。。） => localtime(...) | 函数-Function

#操作系统库函数&常量

# 系统运行（。。。） => system(...) | 函数-Function
# 获取当前目录（。。。） => getcwd(...) | 函数-Function
# 获取进程ID（。。。） => getpid(...) | 函数-Function
# 获取用户ID（。。。） => getuid(...) | 函数-Function
# 获取组ID（。。。） => getgid(...) | 函数-Function
# 更改工作目录（。。。） => chdir(...) | 函数-Function
# 更改权限（。。。） => chmod(...) | 函数-Function
# 更改根目录（。。。） => chroot(...) | 函数-Function
# 重命名（。。。） => rename(...) | 函数-Function
# 删除（。。。） => remove(...) | 函数-Function
# 目录列表（。。。） => listdir(...) | 函数-Function
# 创建目录（。。。） => mkdir(...) | 函数-Function
# 删除目录（。。。） => rmdir(...) | 函数-Function

#命令行库函数&常量
# 参数 => argv | 常量-Constant
# 版本 => version | 常量-Constant
# 平台 => platform | 常量-Constant
# 模块 => modules | 常量-Constant
# 输入流 => __stdin__ | 常量-Constant
# 输出流 => __stdout__ | 常量-Constant
# 。输入（。。。） => .read(...) | 函数-Function
# 。输出（。。。） => .write(...) | 函数-Function
# 。输出在一行（。。。） => .writelines(...) | 函数-Function
# 退出（。。。） => exit(...) | 函数-Function
# 获取对象大小（。。。） => getsizeof(...) | 函数-Function
# 获取默认编码格式（。。。） => getdefaultencoding(...) | 函数-Function
# 获取Windows版本（。。。） => getwindowsversion(...) | 函数-Function

```
