from ..repos import APIRepo


def deploy_template(user, template_name):
    repo = APIRepo()
    return repo.deploy_template(user, template_name)
