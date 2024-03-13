import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.cosmos import CosmosClient
import json
import logging

app = func.FunctionApp()


@app.route(route="GetResumeData/{id:int}", auth_level=func.AuthLevel.ANONYMOUS)
def GetResumeData(req: func.HttpRequest) -> func.HttpResponse:
    # Get the resume id from route params
    id = req.route_params.get('id')
    if not id:
        return func.HttpResponse("Missing id in the function url")

    # Get the resume data from comosdb nosql api
    logging.info(f"Fetching resume data for id: {id}")
    client = CosmosClient(
        url="https://cloud-resume-api-dbacc.documents.azure.com:443",
        credential=DefaultAzureCredential()
    )
    resume_db = client.get_database_client("resume-db")
    container = resume_db.get_container_client("resumes")

    try:
        resume = container.read_item(item=id, partition_key=id)
    except:
        logging.warn("Cannot find a resume with that id")
        return func.HttpResponse(
            status_code=404,
            body="Error finding resume with the given id, please provide a valid resume id"
        )

    return func.HttpResponse(
        status_code=200,
        mimetype="application/json",
        body=json.dumps(resume),
    )
