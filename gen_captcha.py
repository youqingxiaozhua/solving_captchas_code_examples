from captcha.image import ImageCaptcha
import string
import random


def random_str(length=18):
    a = [i for i in string.ascii_letters if i.lower() not in ('i', 'l', 'o')]
    b = [str(i) for i in range(2, 10)]
    a += b
    random.shuffle(a)
    return ''.join(a[:length])


if __name__ == '__main__':
    for i in range(0, 10000):
        rand_str = random_str(4)
        print(rand_str)
        # continue
        img = ImageCaptcha(font_sizes=range(34, 40))
        image = img.generate_image(rand_str)
        # image.show()
        image.save('captcha_images/gen/%s.jpg' % rand_str)



