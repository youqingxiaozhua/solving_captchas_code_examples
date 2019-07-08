# 任务介绍

无论是在爬虫还是自动化项目中，经常会用到登录，而登录又经常会出现图片验证码。
本示例将使用Keras来搭建CNN开山之作——LeNet来破解一个网站的验证码

本实例代码修改自[Adam Geitgey的博文](https://medium.com/@ageitgey/how-to-break-a-captcha-system-in-15-minutes-with-machine-learning-dbebb035a710)

破解验证码的网站：https://www.139130.com/saas/findpwd.html

# 0.前期准备
## 环境搭建
代码在Python3.7的环境下调试通过，但讲道理Python3.x应该都没问题

Python依赖都已记录在requirements.txt中，请尝试执行
```bash
pip install -r requirements.txt
```

**Tips**

本示例程序所需计算量不大，默认安装的是CPU版本的tensorflow，如需使用GPU版本，只需将requirments.txt中的tensorflow修改为tensorflow-gpu即可
## 所需数据
我手动打码了一部分数据，保存在`captcha_images`文件夹下，解压即可，解压后`captcha_images/xuanwu`文件夹下将有大概400多张验证码照片

另外为了充实数据集，我们再使用类似的方法手动生成一些图片便于学习

我们使用Python的captcha库来生成验证码，但其默认生成的验证码带有干扰元素，为了让接下来的分割更容易，我们需要修改captcha包的源代码

> 以下操作非常不建议实践，但我实在太懒了……
> 
> 如果看了一遍之后不太清楚怎么操作，可以放心的忽略，直接进行第1步

1. 找到依赖的安装文件夹，可以执行`where pip`来查看并定位到`Lib\site-packages\captcha\image.py`文件
2. 将image.py的229和230号注释掉，以去掉噪声，like this：
```
227     color = random_color(10, 200, random.randint(220, 255))
228     im = self.create_captcha_image(chars, color, background)
229     # self.create_noise_dots(im, color)
230     # self.create_noise_curve(im, color)
231     im = im.filter(ImageFilter.SMOOTH)
232     return im
```
3. 将image.py的197行注释掉，198行向前缩进一格，以保证所有的字符之间都有空格间隔，否则可能会相互连接在一起
```
 195    images = []
 196    for c in chars:
 197       # if random.random() > 0.5:
 198       images.append(_draw_character(" "))
 199       images.append(_draw_character(c))
```

# 1. 验证码图片分割为单个字符的图片

执行
```bash
python extract_single_letters_from_captchas.py
```

为了减少机器学习的工作量，我们将验证码图片分割为4个字符的图片
分割的图片将保存在extracted_letter_images文件夹中

# 2. 训练模型

```bash
python train_model.py
```
可能需要十几分钟的时间，如果感兴趣也可以尝试采用其他模型，比如常规的线性回归到更深的神经网络

# 3. 用训练好的模型识别验证码

```bash
python solve_captchas_with_model.py
```


