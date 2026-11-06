# locustfile.py
from locust import HttpUser, task, between

class TaskFlowUser(HttpUser):
    wait_time = between(0.5, 2.0)

    def on_start(self):
        """Create a parent project for task operations on user init."""
        response = self.client.post("/projects/", json={"name": "Load Test Project", "owner_id": 1})
        if response.status_code == 201:
            self.project_id = response.json()["id"]
        else:
            self.project_id = 1

    @task(4)  # Executed 4x more often
    def list_tasks(self):
        self.client.get(f"/projects/{self.project_id}/tasks/?skip=0&limit=20")

    @task(1)
    def create_and_update_task(self):
        # Create
        res = self.client.post(
            f"/projects/{self.project_id}/tasks/",
            json={"title": "Locust Task", "priority": 3}
        )
        if res.status_code == 201:
            task_id = res.json()["id"]
            # Update
            self.client.patch(
                f"/projects/{self.project_id}/tasks/{task_id}",
                json={"completed": True}
            )