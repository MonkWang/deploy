# coding=utf-8
from deploy import Deploy

if __name__ == '__main__':
    obj = Deploy("/data/www/html")
    print("result", obj.refresh_cdn())
