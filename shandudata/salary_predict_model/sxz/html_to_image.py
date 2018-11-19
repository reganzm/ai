# coding:utf-8
'''
Created on 2015年1月7日

@author: likaiguo
@summary: 通过url访问,通过splinter的phantomjs驱动完成截图,保存到本地
            使用PIL-Piillow进行图像处理返回
'''

import os
from time import sleep

from PIL import Image
from splinter import Browser


BROWSER_DRIVER = 'phantomjs'


def html2image(url, name, save_dir, suffix='.png'):
    browser = Browser(BROWSER_DRIVER)
    browser.visit(url)
    sleep(2)
    real_path_head = os.path.join(save_dir, name)
    image_path = browser.screenshot(real_path_head, suffix)
    browser.quit()

    return image_path


def image_crop(image_path, height=None, width=None, box=()):
    """
    @summary: 图片切割
    传入宽度,按中间向两边分割
    传入高度,也按照中线向两边分割
    传入box,(left,upper,right,lower) 坐上右下左边,则忽略前两个指标
    """
    im = Image.open(image_path)

    if not box:
        w, h = im.size
        if width:
            width = int(width)
            left, right = (w - width) / 2, (w + width) / 2
        else:
            left, right = 0, w
        if height:
            height = int(height)
            upper, lower = (h - height) / 2, (h + height) / 2
        else:
            upper, lower = 0, h
        box = (left, upper, right, lower)
    image_path, ext = os.path.splitext(image_path)
    new_image = im.crop(box)
    save_path = '%s_%s%s' % (image_path, '%d_%d_%d_%d' % box, ext)

    new_image.save(save_path)

    return save_path


if __name__ == '__main__':

    import json
    d = {"id": "54ad019e12298209fb2991e6", "platform": "wb", "url":
        "http://www.baidu.com/s?wd=hello&rsv_spt=1&issp=1&f=8&rsv_bp=0&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_sug3=6&rsv_sug4=448&rsv_sug1=2&rsv_pq=c9c3086900006794&rsv_t=3e7d9iUU59IeZCCGnzd8OXbZPKCw9wvl%2FA%2FdGpkqKKnX8MExEhK2igf9mom8TB3kC8YH&rsv_sug2=0&inputT=2837"}
    print json.dumps(d)

    path = '/home/likaiguo/'
    image_path = html2image(url='http://www.baidu.com', name='baidu', save_dir=path)
    save_path = image_crop(image_path, height=400, width=400)
    print save_path
