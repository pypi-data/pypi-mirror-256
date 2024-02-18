from ..repos import APIRepo


def stop_service(user, project, service_id):
    repo = APIRepo()
    service = repo.retrieve_service(user, service_id)
    print(f"Stopping service {service['type']}/{service['name']} ...")
    return repo.stop_service(user, service_id)


def stop_service_by_name(user, project, service_type, service_name):
    repo = APIRepo()
    data, error = repo.retrieve_project_by_name(user, project)
    print(f"Stopping service {service_type}/{service_name} ...")
    data, error = repo.stop_service_by_name(
        user, data["id"], service_type, service_name
    )
    if error:
        raise Exception("Something went wrong.\n" + error)
    return data
