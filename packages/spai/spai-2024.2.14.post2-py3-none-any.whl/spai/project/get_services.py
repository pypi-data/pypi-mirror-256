from ..repos import APIRepo


def get_services(user, project_name):
    repo = APIRepo()
    data, error = repo.retrieve_project_by_name(user, project_name)
    if data:
        return data["services"]
    raise Exception("Something went wrong.\n" + error)
