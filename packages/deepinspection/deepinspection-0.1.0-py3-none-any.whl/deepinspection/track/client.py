from __future__ import annotations

import json
from typing import Generator, List

import requests
from pydantic import BaseModel


class Fastenings(BaseModel):
    client: DeepInspectionTrackClient

    def list(self) -> List[dict]:
        url = f"{self.client.base_url()}/exports/fastenings"
        response = requests.get(url, headers=self.client.auth_headers())
        response.raise_for_status()
        return response.json()

    def get(self, export_id) -> dict:
        url = f"{self.client.base_url()}/exports/fastenings/{export_id}"
        response = requests.get(url, headers=self.client.auth_headers())
        response.raise_for_status()
        return response.json()

    def get_data(self, export_id) -> Generator[dict, None, None]:
        url = f"{self.client.base_url()}/exports/fastenings/{export_id}/data"
        response = requests.get(
            url,
            headers={
                **self.client.auth_headers(),
                "Accept": "application/x-ndjson",
            },
            stream=True,
        )
        response.raise_for_status()

        for line in response.iter_lines():
            if line:
                yield json.loads(line.decode("utf-8"))


class Exports(BaseModel):
    client: DeepInspectionTrackClient

    @property
    def fastenings(self):
        return Fastenings(client=self.client)


class DeepInspectionTrackClient(BaseModel):
    customer_id: str
    client_id: str
    client_secret: str

    def base_url(self):
        return (
            f"https://{self.customer_id}.api.track.deepinspection.io/external/v0-alpha"
        )

    def auth_headers(self):
        return {
            "Authorization": f"Bearer {self.access_token()}",
            "X-Customer-ID": self.customer_id,
        }

    def openid_connect_url(self):
        return f"https://auth.nextml.com/auth/realms/deepinspection-track-{self.customer_id}/.well-known/openid-configuration"

    def access_token(self) -> str:
        response = requests.get(self.openid_connect_url())
        if response.status_code != 200:
            raise Exception("Failed to authenticate with OIDC")

        oidc_discoveries = response.json()
        token_url = oidc_discoveries["token_endpoint"]

        response = requests.post(
            token_url,
            data=dict(grant_type="client_credentials"),
            auth=(self.client_id, self.client_secret),
        )

        if response.status_code != 200:
            raise Exception(
                f"Failed to authenticate, status code {response.status_code}, text {response.text}"
            )

        return response.json()["access_token"]

    @property
    def exports(self):
        return Exports(client=self)
