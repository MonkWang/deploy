from deploy import Deploy

if __name__ == '__main__':
    obj = Deploy("/data/www/html")
    obj.refresh_cdn()
