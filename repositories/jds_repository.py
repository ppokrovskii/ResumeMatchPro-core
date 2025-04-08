import logging
from typing import Optional, Any
from uuid import UUID

from azure.cosmos import DatabaseProxy, PartitionKey  # type: ignore
from azure.cosmos.exceptions import CosmosHttpResponseError  # type: ignore
from repositories.models import JobDescriptionDb
from shared.exceptions import PermissionDeniedError


class JobDescriptionRepository:
    def __init__(self, db_client: DatabaseProxy):
        container_id = "job_descriptions"
        unique_key_policy = {"uniqueKeys": [{"paths": ["/user_id", "/title", "/company"]}]}
        partition_key = PartitionKey(path="/user_id")
        self.container = db_client.create_container_if_not_exists(
            id=container_id,
            unique_key_policy=unique_key_policy,
            partition_key=partition_key,
        )

    def upsert_job_description(self, job_description: dict[str, Any]) -> JobDescriptionDb:
        logging.info(f"Upserting job description: {job_description}")
        # Convert is_active to string if it's a boolean
        if "is_active" in job_description and isinstance(job_description["is_active"], bool):
            job_description["is_active"] = str(job_description["is_active"]).lower()

        # Query to check if a document with the same user_id, title and company exists
        query = """
            SELECT * FROM c
            WHERE c.user_id = @user_id
            AND c.title = @title
            AND c.company = @company
        """
        parameters: list[dict[str, Any]] = [
            {"name": "@user_id", "value": job_description["user_id"]},
            {"name": "@title", "value": job_description["title"]},
            {"name": "@company", "value": job_description["company"]},
        ]
        items = list(self.container.query_items(query, parameters=parameters))
        if items:
            # Update the existing document
            job_description["id"] = items[0]["id"]
            result = self.container.upsert_item(job_description)
        else:
            # Create a new document
            result = self.container.upsert_item(job_description)
        logging.info(f"Upserted job description result: {result}")
        return JobDescriptionDb(**result)

    def get_job_descriptions(self, user_id: str, is_active: Optional[bool] = None) -> list[JobDescriptionDb]:
        query = "SELECT * FROM c WHERE c.user_id = @user_id"
        parameters: list[dict[str, Any]] = [{"name": "@user_id", "value": user_id}]

        if is_active is not None:
            query += " AND c.is_active = @is_active"
            parameters.append({"name": "@is_active", "value": str(is_active).lower()})

        logging.info(f"Executing query: {query} with parameters: {parameters}")
        items = list(self.container.query_items(query=query, parameters=parameters))
        logging.info(f"Found {len(items)} items: {items}")
        return [JobDescriptionDb(**item) for item in items]

    def delete_all(self) -> None:
        items = list(self.container.read_all_items())
        for item in items:
            self.container.delete_item(item, partition_key=item["user_id"])

    def delete_job_description(self, user_id: str, job_description_id: str | UUID) -> bool:
        """Delete a job description by user_id and job_description_id."""
        if isinstance(job_description_id, UUID):
            job_description_id = str(job_description_id)

        try:
            # First check if job description exists for any user
            query = "SELECT * FROM c WHERE c.id = @job_description_id"
            parameters: list[dict[str, Any]] = [{"name": "@job_description_id", "value": job_description_id}]
            items = list(
                self.container.query_items(
                    query, parameters=parameters, enable_cross_partition_query=True
                )
            )
            if not items:
                return False

            job_description = JobDescriptionDb(**items[0])
            if job_description.user_id != user_id:
                raise PermissionDeniedError(
                    "You don't have permission to access this job description"
                )

            self.container.delete_item(item=job_description_id, partition_key=user_id)
            return True

        except CosmosHttpResponseError as e:
            raise e

    def get_job_description_by_id(self, user_id: str, job_description_id: str | UUID) -> Optional[JobDescriptionDb]:
        """Get a job description by user_id and job_description_id."""
        if isinstance(job_description_id, UUID):
            job_description_id = str(job_description_id)

        try:
            # First check if job description exists for any user
            query = "SELECT * FROM c WHERE c.id = @job_description_id"
            parameters: list[dict[str, Any]] = [{"name": "@job_description_id", "value": job_description_id}]
            items = list(
                self.container.query_items(
                    query, parameters=parameters, enable_cross_partition_query=True
                )
            )
            if not items:
                return None

            job_description = JobDescriptionDb(**items[0])
            if job_description.user_id != user_id:
                raise PermissionDeniedError(
                    "You don't have permission to access this job description"
                )
            return job_description

        except CosmosHttpResponseError as e:
            raise e
