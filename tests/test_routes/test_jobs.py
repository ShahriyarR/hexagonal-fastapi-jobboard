from fastapi import status
from fastapi.encoders import jsonable_encoder

from src.jobboard.domain.schemas.jobs import JobCreateInputDto, JobOutputDto


def test_create_job(client, normal_user_token_headers, app, get_fake_container):
    data = {
        "title": "SDE super",
        "company": "doogle",
        "company_url": "www.doogle.com",
        "location": "USA,NY",
        "description": "python",
        "date_posted": "2022-03-20",
    }
    data = JobCreateInputDto(**data)
    with app.container.job_service.override(get_fake_container.fake_job_service):
        with app.container.user_service.override(get_fake_container.fake_user_service):
            response = client.post(
                "/jobs/create-job/",
                json=jsonable_encoder(data),
                headers=normal_user_token_headers,
            )
            assert response.status_code == 200
            assert response.json()["company"] == "doogle"
            assert response.json()["description"] == "python"


def test_read_job(client, normal_user_token_headers, get_fake_container, app):
    data = {
        "title": "SDE super",
        "company": "doogle",
        "company_url": "www.doogle.com",
        "location": "USA,NY",
        "description": "python",
        "date_posted": "2022-03-20",
    }
    data = JobCreateInputDto(**data)
    with app.container.job_service.override(get_fake_container.fake_job_service):
        with app.container.user_service.override(get_fake_container.fake_user_service):
            response = client.post(
                "/jobs/create-job/",
                json=jsonable_encoder(data),
                headers=normal_user_token_headers,
            )
            assert response.status_code == 200
            response = client.get("/jobs/get/1/")
            assert response.status_code == 200
            assert response.json()["title"] == "SDE super"


def test_read_jobs(client, normal_user_token_headers, get_fake_container, app):
    data = {
        "title": "SDE super",
        "company": "doogle",
        "company_url": "www.doogle.com",
        "location": "USA,NY",
        "description": "python",
        "date_posted": "2022-03-20",
    }
    data = JobCreateInputDto(**data)
    with app.container.job_service.override(get_fake_container.fake_job_service):
        with app.container.user_service.override(get_fake_container.fake_user_service):
            client.post(
                "/jobs/create-job/",
                json=jsonable_encoder(data),
                headers=normal_user_token_headers,
            )
            client.post(
                "/jobs/create-job/",
                json=jsonable_encoder(data),
                headers=normal_user_token_headers,
            )

            response = client.get("/jobs/all/")
            assert response.status_code == 200
            assert response.json()[0]
            assert response.json()[1]


def test_update_a_job(client, normal_user_token_headers, get_fake_container, app):
    data = {
        "title": "New Job super",
        "company": "doogle",
        "company_url": "www.doogle.com",
        "location": "USA,NY",
        "description": "fastapi",
        "date_posted": "2022-03-20",
    }
    data = JobCreateInputDto(**data)
    with app.container.job_service.override(get_fake_container.fake_job_service):
        with app.container.user_service.override(get_fake_container.fake_user_service):
            client.post(
                "/jobs/create-job/",
                json=jsonable_encoder(data),
                headers=normal_user_token_headers,
            )
            data.title = "test new title"
            response = client.put("/jobs/update/1", json=jsonable_encoder(data))
            assert response.json()["msg"] == "Successfully updated data."
            response = client.put("/jobs/update/85", json=jsonable_encoder(data))
            assert response.json()["detail"] == "Job with id 85 not found"
            assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_a_job(client, normal_user_token_headers, get_fake_container, app):
    data = {
        "title": "New Job super",
        "company": "doogle",
        "company_url": "www.doogle.com",
        "location": "USA,NY",
        "description": "fastapi",
        "date_posted": "2022-03-20",
    }
    data = JobCreateInputDto(**data)
    with app.container.job_service.override(get_fake_container.fake_job_service):
        with app.container.user_service.override(get_fake_container.fake_user_service):
            client.post(
                "/jobs/create-job/",
                json=jsonable_encoder(data),
                headers=normal_user_token_headers,
            )
            client.delete("/jobs/delete/1", headers=normal_user_token_headers)
            response = client.get("/jobs/get/1/")
            assert response.status_code == status.HTTP_404_NOT_FOUND
            response = client.delete(
                "/jobs/delete/85", headers=normal_user_token_headers
            )
            assert response.status_code == status.HTTP_404_NOT_FOUND
