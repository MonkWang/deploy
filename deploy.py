# coding=utf-8
import os
import sys
import getopt
import constants
from fabric import Connection
from aliyunsdkcore.client import AcsClient
from aliyunsdkcdn.request.v20180510.RefreshObjectCachesRequest import RefreshObjectCachesRequest
import hashlib
from fabric import SerialGroup as Group


class Deploy:
    def __init__(self, www_dir):
        self.www_dir = www_dir

    @staticmethod
    def get_param():
        project_name = ''
        code = ''
        server = ''
        branch = None
        opts, args = getopt.getopt(sys.argv[1:], 'd:s:b:')
        for op, value in opts:
            if op == '-d':
                project_name = value
                code += '/' + value
            elif op == '-s':
                server = value
            elif op == '-b':
                branch = value
        return project_name, server, branch

    def pull(self):
        project_name, server, branch = self.get_param()
        code = constants.CODE_DIR + '/' + project_name
        commit = None
        if not branch is None:

            if branch.find('/') == -1:
                commit = branch
            code = self.get_real_code_dir(project_name, branch)
            if not os.path.exists(code):
                os.makedirs(code, exist_ok=True)
                os.system('git clone ssh://gogs@gogs.developer.shengxintech.com:8089/' + project_name + '.git ' + code)
                os.chdir(code)
                os.system('git checkout -b ' + branch[branch.index('/') + 1:])

            os.chdir(code)
            print(code)
            if not commit is None:
                os.system('git fetch --all')
                os.system('git reset --hard ' + commit)
            else:
                os.system('git fetch --all')
                os.system('git reset --hard ' + branch)
            is_sxtest2 = server.find('sxtest2') != -1
            if is_sxtest2:
                os.system('chown -Rf nginx:nginx ' + code)
            else:
                os.system('chown -Rf www:www ' + code)
            # os.system('chmod -R 755 ' + code)

    def get_real_code_dir(self, project_name, branch):
        code = constants.CODE_DIR + '/' + project_name
        if branch.find('/') != -1:
            code += '_' + branch[branch.index('/') + 1:]
        else:
            code += 'default_reset'
        return code

    def deploy(self, type, handle=None):
        project_name, server, branch = self.get_param()
        name = project_name[project_name.index('/') + 1:]
        is_test = server.find('test') != -1
        print("是否sxtest2:%s", 'sxtest2' == server)
        # if 'sxtest2' == server:
        #     self.www_dir = '/web/www'
        project = self.www_dir + '/' + name
        code = self.get_real_code_dir(project_name, branch)
        os.chdir(code)

        if type is constants.BACKEND:
            if is_test:
                if os.system('/usr/local/bin/composer install') != 0:
                    exit(1)
                if os.system('/bin/cp -f .env.test .env') != 0:
                    exit(1)
            else:
                if os.system('composer install --no-dev') != 0:
                    exit(1)
                if os.system('/bin/cp -f .env.production .env') != 0:
                    exit(1)
        elif type is constants.FRONTEND:

            code_md5 = hashlib.md5(code.encode(encoding="UTF-8")).hexdigest()
            file = '/tmp/' + code_md5 + '.txt'
            lock = open(code + '/package.json', 'r')
            current = hashlib.md5(
                lock.read().replace("\n", '').replace(' ', '').encode(encoding="UTF-8")).hexdigest()
            if os.path.exists(file):
                f = open(file, 'r+')
                up = f.read()
                if up != current:
                    os.system('npm config get registry')
                    os.system('npm install')
                else:
                    print("不需要npm install")
            else:
                f = open(file, 'w')
                os.system('npm install')
            f.seek(0)
            f.truncate()
            f.write(current)
            f.close()
            lock.close()
            if is_test:
                ret = os.system('npm run build-dev')
            else:
                ret = os.system('npm run build')
            if ret != 0:
                exit(1)
        server_name = server
        server = 'root@' + server
        print("serverName:", server)
        for c in Group(*server.split(','), forward_agent=True):
            # pass
            # with Connection(host=server, forward_agent=True) as c:
            if type is constants.FRONTEND:
                c.run('rsync -avz --exclude "node_modules/" --delete root@%s:%s/ %s ' % (
                    constants.JUMP_SERVER_IP, code, project))
                with c.cd(project):
                    pass
            elif type is constants.BACKEND:
                delete = '--delete' if is_test else ''
                c.run(
                    'rsync -avz -e "ssh -o StrictHostKeyChecking=no" --include="storage/" --include="storage/framework/" --include="storage/framework/*" --exclude="storage/*" --exclude="public/storage"  %s root@%s:%s/ %s' % (
                        delete, constants.JUMP_SERVER_IP, code, project))
                with c.cd(project):
                    # c.run('redis-cli set gray on')
                    c.run('php artisan migrate --force')
                    ret = 'supervisorctl reload'
                    if server_name in constants.DOCKER_SERVER:
                        # c.run('chmod -R 777 %s' % project)
                        c.run('docker exec php-web %s' % ret)
                        c.run('docker exec php-cli %s' % ret)
                    else:
                        c.run(ret)
                    # c.run('redis-cli set gray off')
        if not handle is None:
            handle(project_name, server, branch)

    def refresh_cdn(self):
        project_name, server, _ = self.get_param()
        if project_name != 'heplus/heplus-frontend':
            return
        if server != 'heplus':
            return
        client = AcsClient(constants.ALIYUN_OSS_ACCESS_KEY_ID, constants.ALIYUN_OSS_ACCESS_KEY_SECRET, 'cn-hangzhou')
        request = RefreshObjectCachesRequest()
        request.set_accept_format('json')
        request.set_ObjectPath(constants.HEPLUS_URL)
        response = client.do_action_with_exception(request)
        return str(response, encoding='utf-8')
