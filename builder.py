from fswrap import File, Folder
from gitbot import stack
from gitbot.lib import hyde
from gitbot.lib.s3 import Bucket
from gitbot.lib.git import Tree
import yaml


def pull(source, repo, branch):
    tree = Tree(source, repo=repo, branch=branch)
    tree.clone(tip_only=True)


def __upload(proj, repo, branch, data, maker, force=True):
    root = Folder(data.root or '~')
    source = root.child_folder('src').child_folder(proj)
    dist = root.child_folder('dist')
    b = Bucket(data.bucket)
    b.make()
    key_folder = Folder(data.project).child_folder(branch)
    zippath = dist.child_file(proj + '.zip')
    key_path = key_folder.child(zippath.name)
    key = b.bucket.get_key(key_path)
    if force or not key:
        target = dist.child_folder(proj)
        pull(source, repo, branch)
        target.make()
        maker(source, target)
        target.zip(zippath.path)
        b.add_file(zippath, target_folder=key_folder.path)
        key = b.bucket.get_key(key_folder.child(zippath.name))
    return key.generate_url(30000)


def upload_www(data, force=True):

    def maker(source, target):
        hyde.gen(source, data, target=target.path)

    return __upload('www', data.www_repo, data.www_branch, data, maker, force)


def upload_app(data, force=True):

    def maker(source, target):
        stuff = ['apps', 'lib', 'app.js', 'package.json']
        for f in stuff:
            fs = Folder.file_or_folder(source.child(f))
            fs.copy_to(target)

    return __upload('app', data.app_repo, data.app_branch, data, maker, force)


def publish(data, push_www=True, push_app=False):
    www_archive = upload_www(data, push_www)
    app_archive = upload_app(data, push_app)
    config_file = File(File(__file__).parent.child('stack/gitbot.yaml'))
    config = yaml.load(config_file.read_all())
    config['file_path'] = config_file.path
    params = data.get('stack_params', dict())
    params.update(dict(AppSource=app_archive, WebSource=www_archive))
    config['data'] = data
    stack.publish_stack(config,
                        params=params,
                        debug=True,
                        wait=True)
