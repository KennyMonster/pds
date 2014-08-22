"""
Common tasks that can be performed locally or on a dev/production server
for easy deployment
"""
import os
from fabric.api import local, cd, run, lcd
from fabric.context_managers import prefix, shell_env
from fabric.operations import sudo
from fabric.state import env


dev_server_code_path = '/www/pds'
dev_server_venv_path = '/www/venv_pds/'

prod_server_code_path = dev_server_code_path

django_project_path = 'project3'


# Funcitons to set roles


def dev():
    env.hosts = ['sctc@pds.liquefied.net']


def push():
    # test()
    local('git push origin HEAD')


def pull():
    local('git pull')


def freeze():
    local('pip freeze > requirements.txt')


def pip_install_requirements():
    # OSX needs this for several packages to build correctly
    with shell_env(ARCHFLAGS='-Wno-error=unused-command-line-argument-hard-error-in-future'):
        local('pip install -r requirements.txt')


def schema_migration(app):
    """
    Migrate and apply South schema migration
    """
    with lcd(django_project_path):
        local('./manage.py schemamigration %s --auto' % app)
        local('./manage.py migrate %s' % app)


def migrate():
    """
    Call both syncdb and migrate on the DB
    """
    with lcd(django_project_path):
        local('./manage.py syncdb --noinput')
        local('./manage.py migrate')


def createsuperuser():
    """
    Create an admin account on the site
    """
    with lcd(django_project_path):
        local('./manage.py createsuperuser')


def collectstatic():
    """
    Collect static media
    """
    with lcd(django_project_path):
        local('./manage.py collectstatic --noinput')


def test():
    """
    Run automated tests
    """
    with lcd(django_project_path):
        local('./manage.py test file_manager')


def restart_server():
    """
    Restarts a public server
    """
    sudo('supervisorctl restart project3')


def runserver():
    """
    Runs the Django dev server locally
    """
    with lcd(django_project_path):
        local('./manage.py runserver')


def update_dev_env():
    """
    Installs all python requirements, migrates the DB, loads all fixtures, locally
    """
    pip_install_requirements()
    migrate()


def deploy():
    """
    Deploy code to the live server
    """
    push()
    with cd(dev_server_code_path), prefix('source ' + os.path.join(dev_server_venv_path, 'bin', 'activate')):
        run('fab pull')
        run('pip install -r requirements.txt')
        run('fab migrate')
        run('fab load_fixtures')
    restart_server()


# def deploy_prod():
#     """
#     Deploy code to production server
#     """
#     push()
#     with cd(prod_server_code_path):
#         run('fab pull')
#         run('pip install -r requirements.txt')
#         run('fab migrate')
#         run('fab collectstatic')
#     restart_server()
