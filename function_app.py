import azure.functions as func

app = func.FunctionApp()


@app.route(route="GetResumeData/{id}", auth_level=func.AuthLevel.ANONYMOUS)
@app.cosmos_db_input(
    arg_name="resume",
    database_name="resume-db",
    container_name="resumes",
    id="{id}",
    partition_key="{id}",
    connection="CosmosDbConnectionSetting"
)
def GetResumeData(req: func.HttpRequest, resume: func.DocumentList) -> func.HttpResponse:
    return func.HttpResponse(
        status_code=200,
        mimetype="application/json",
        body=resume[0].to_json()
    )
