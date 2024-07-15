# locustfile.py
from locust import HttpUser, task, between


class WebsiteTestUser(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def my_task(self):
        test_access_token = ''
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {test_access_token}'
        }
        ticket_id = 3
        self.client.post(f"/api/tickets/{ticket_id}/purchase/",
                         headers=headers,
                         json={'quantity': 1})