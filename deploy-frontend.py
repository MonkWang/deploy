#!/usr/bin/env python
# coding=utf-8

from deploy import Deploy

if __name__ == '__main__':
    obj = Deploy("/data/www")
    obj.deploy(2)
