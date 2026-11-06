# tests/test_functional.py

def test_create_and_get_task_flow(client):
    # 1. Setup prerequisite Project (assuming /projects endpoint exists)
    proj_resp = client.post("/projects/", json={"name": "Test Project", "owner_id": 1})
    assert proj_resp.status_code == 201
    project_id = proj_resp.json()["id"]

    # 2. Create Task
    task_payload = {"title": "Deploy API", "description": "Uvicorn setup", "priority": 1}
    create_resp = client.post(f"/projects/{project_id}/tasks/", json=task_payload)
    assert create_resp.status_code == 201
    task_id = create_resp.json()["id"]

    # 3. Retrieve Task
    get_resp = client.get(f"/projects/{project_id}/tasks/{task_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == "Deploy API"

def test_get_task_not_found(client):
    response = client.get("/projects/999/tasks/999")
    assert response.status_code == 404