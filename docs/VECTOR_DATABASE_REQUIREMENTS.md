## Purpose

Integrate a DigitalOcean Managed OpenSearch Vector Database into the MVP to compute a resume–job-description similarity score.
Only one document is stored at a time and overwritten each submission.
No user accounts or persistent history.

## Technology

    •	DigitalOcean Managed OpenSearch (vector-enabled)
    •	Accessed from FastAPI using opensearch-py
    •	Embeddings generated in FastAPI (OpenAI or DO embeddings)
    •	Similarity calculated by OpenSearch (Vector Search)

## Connection Details Required

To connect the application to the DigitalOcean Managed OpenSearch cluster, the following configuration details are needed. Please provide these variables (likely via a `.env` file or environment variables):

*   **DO_OPENSEARCH_HOST**: The hostname of your cluster.
    *   *Example*: `db-postgresql-nyc1-12345-do-user-12345-0.b.db.ondigitalocean.com` (Note: for OpenSearch it will look similar but likely contain `opensearch`)
    *   *Real Example*: `c-name-do-user-12345-0.b.db.ondigitalocean.com`
*   **DO_OPENSEARCH_PORT**: The port number.
    *   *Example*: `25060`
*   **DO_OPENSEARCH_USERNAME**: The username for the database.
    *   *Example*: `doadmin`
*   **DO_OPENSEARCH_PASSWORD**: The password for the database.
    *   *Example*: `AVNS_D5...` (a long random string)
*   **DO_OPENSEARCH_SERVICE_URI**: (Optional) sometimes provided as a full connection string.
    *   *Example*: `https://doadmin:password@host:port`

## Overview of DigitalOcean Managed OpenSearch Vector Database

Our MVP application is a Python FastAPI app, that currently has two screens. The first where the user uploads their resume (docx file) and job description. The user hits submit and goes to the next page where the user is presented with a new resume, cover letter, and pointers for how to make their resume better. There are also currently placeholders for “Resume Qualifier Match” which will be the calculated by this vectorized similarity score on the user’s original resume and the posted job description.

Our MVP does not have a login or user table.

This way when the user submits their resume and job description it will upload to a single table in the DigitalOcean Vector Store database called resume_and_descripition_embeddings. Then it will have one row with two columns one for resume_embedding and the second column job_description_embedding.

The embedding scores are created for these data and returned to the website to display. When another user or the same user starts again, the single row in the vector database will be overridden with the new data.

That way at most there will only be one user at all time and no email is stored.

The second page also has a “Resume Qualifier Match REVISED” but for now let’s leave that as a placeholder.

I have attached the CLAUDE.md file that details information about the code base.

Would you create a VECTOR_DATABASE_REQUIREMENTS.md file that I can download with specifications for our engineers to build this functionality into our MVP. If anything is not clear please ask clarifying questions.
