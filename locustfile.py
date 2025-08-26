from locust import HttpUser, task, between

class FastAPIUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def ping(self):
        self.client.get("/ping")
