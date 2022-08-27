from fabric.api import local, task


@task
def clean():
    local("rm -rf build dist *.egg django_route/__pycache__ django_route/*.pyc")


@task
def bump_version(part="patch"):
    local("bumpversion {}".format(part))
    local("git push")
    local("git push --tags")


@task
def release(part="patch"):
    bump_version(part=part)
    pypi()


@task
def pypi():
    clean()
    local("poetry publish --build")
