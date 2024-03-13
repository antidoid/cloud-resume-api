import azure.functions as func
import json

app = func.FunctionApp()


@app.route(route="GetResumeData/{id}", auth_level=func.AuthLevel.ANONYMOUS)
@app.cosmos_db_input(
    arg_name="resume",
    database_name="resume-db",
    container_name="resumes",
    id="{id}",
    partition_key="{id}",
    connection="connect"
)
def GetResumeData(req: func.HttpRequest, resume: func.DocumentList) -> func.HttpResponse:
    # If there is no document with the provided id
    if not resume:
        return func.HttpResponse(
            status_code=404,
            mimetype="application/json",
            body=json.dumps(
                {"message": "Resume not found, please try a valid resume id"})
        )

    # Provide the resume data from the found document
    return func.HttpResponse(
        status_code=200,
        mimetype="application/json",
        body=resume[0].to_json()
    )
