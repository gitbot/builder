from boto.exception import BotoServerError
from fswrap import File, Folder
from gitbot import stack
from gitbot.conf import ConfigDict
from gitbot.lib import hyde
from gitbot.lib.s3 import Bucket
from gitbot.lib.git import Tree
import yaml


def get_worker_outputs(data):
    result = None
    try:
        worker_stack_name = data.worker_stack_name or 'gitbot-worker'
        region = data.region or 'us-east-1'
        root = Folder(data.root or '~')
        source = root.child_folder('src')
        source.make()
        source = source.child_folder('worker')
        repo = data.worker_repo or 'git://github.com/gitbot/worker.git'
        branch = data.worker_branch or 'master'

        #   1. Pull worker repo
        tree = Tree(source, repo, branch)
        tree.clone(tip_only=True)

        #   2. Call gitbot.stack.publish with 'gitbot.yaml'
        stack.publish_stack(source.child_file('gitbot.yaml'), wait=True)
        result = stack.get_outputs(worker_stack_name, region)
    except Exception, e:
        print repr(e)
        raise
    finally:
        source.delete()
        return result 


def check_revision_already_published(proj, bucket_name, tree):
    b = Bucket(bucket_name)
    if not b.connect():
        return None
    
    sha = tree.get_revision_remote()
    key_folder = Folder(proj).child_folder(tree.branch_name)
    key_folder = key_folder.child_folder(sha)
    key_path = key_folder.child(proj + '.zip')
    return b.bucket.get_key(key_path)

def __upload(proj, repo, branch, data, maker, force=True):
    root, source, dist = (None, None, None)
    try:
        root = Folder(data.root or '~')
        source = root.child_folder('src')
        source.make()
        source = source.child_folder(proj)
        dist = root.child_folder('dist')
        tree = Tree(source, repo=repo, branch=branch)
        key = None
        if not force: 
            key = check_revision_already_published(proj, data.bucket, tree)

        if not key:
            b = Bucket(data.bucket)
            b.make()
            key_folder = Folder(proj).child_folder(branch)
            zippath = dist.child_file(proj + '.zip')
            tree.clone(tip_only=True)
            sha = tree.get_revision(short=False)
            key_folder = key_folder.child_folder(sha)
            target = dist.child_folder(proj)
            target.make()
            maker(source, target)
            target.zip(zippath.path)
            b.add_file(zippath, target_folder=key_folder.path)
            key = b.bucket.get_key(key_folder.child(zippath.name))
    finally:
        if source:
            source.delete()
        if dist:
            dist.delete()

    return key.generate_url(30000)


def upload_www(data, force=True):

    def maker(source, target):
        hyde.gen(source, ConfigDict(dict(data=data)), target=target.path)

    return __upload('www', data.www_repo, data.www_branch, data, maker, force)


def upload_app(data, force=True):

    def maker(source, target):
        stuff = ['apps', 'lib', 'app.js', 'package.json']
        for f in stuff:
            fs = Folder.file_or_folder(source.child(f))
            fs.copy_to(target)

    return __upload('app', data.app_repo, data.app_branch, data, maker, force)


def publish(data, push_www=True, push_app=False):
    data = ConfigDict(data)
    www_archive = upload_www(data, push_www)
    app_archive = upload_app(data, push_app)
    config_file = File(File(__file__).parent.child('stack/gitbot.yaml'))
    config = yaml.load(config_file.read_all())
    config['file_path'] = config_file.path
    params = data.get('stack_params', dict())
    params.update(dict(AppSource=app_archive, WebSource=www_archive))
    worker_params = get_worker_outputs(data)
    if not worker_params or 'QueueURL' not in worker_params:
        raise Exception('Failed to create the worker stack')
    params.update(dict(
        WorkerQueueURL=worker_params['QueueURL'],
        ManagerAccessKey=worker_params['ManagerKey'],
        ManagerSecretKey=worker_params['ManagerSecret']
    ))
    config['data'] = data
    stack.publish_stack(config,
                        params=params,
                        wait=True)

def validate(data):
    data = ConfigDict(data)
    config_file = File(File(__file__).parent.child('stack/gitbot.yaml'))
    config = yaml.load(config_file.read_all())
    config['file_path'] = config_file.path
    stack.validate_stack(config)


