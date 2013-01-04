import actions
import yaml
from gitbot.conf import ConfigDict


def test_run():
    data_yaml = \
'''
root: ~/tmp/gen
bucket: gitbot_test
project: gitbot/gitbot
app_repo: git://github.com/gitbot/api.git
app_branch: master
www_repo: git://github.com/gitbot/www.git
www_branch: master
app_key: apartment-user
app_ip: 23.23.141.185
app_domain: extrazeal.com
githubClientId: c62353d0f816a5f3f50f
githubClientSecret: c6559170c9f43bd225138fbfabf8ce1d4e37c5f8
'''
    data = ConfigDict(yaml.load(data_yaml))
    actions.update(data)

if __name__ == '__main__':
    test_run()
