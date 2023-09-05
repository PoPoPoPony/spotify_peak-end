from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
import Levenshtein
import glob
from backend.statistics.main import main as statistics_main
import os



router = APIRouter(
    prefix='/api/v1/temp',
    tags = ["temp usage"]
)



@router.get("/{temp_file_name}", response_class=FileResponse)
def get_temp_file(temp_file_name: str):
    file_path = f"backend/static/{temp_file_name}"
    is_exist = os.path.exists(file_path)

    if is_exist:
        return FileResponse(path=file_path, filename=temp_file_name)
    else:
        all_file_paths = glob.glob("backend/static/*")
        i=0
        max_similarity = -1
        max_similarity_i = 0
        for i in range(len(all_file_paths)):
            similarity = Levenshtein.ratio(file_path, all_file_paths[i])
            if similarity > max_similarity:
                max_similarity = similarity
                max_similarity_i = i

        html_content = f"""
            <html>
                <head>
                    <title>File not found QwQ</title>
                </head>
                <body>
                    <h1>Did you mean <span style='color: red'>{os.path.split(all_file_paths[max_similarity_i])[-1]}</span>?</h1>
                </body>
            </html>
        """

        return HTMLResponse(content=html_content, status_code=404)
    


@router.post("/update_statistic_files")
def update_statistic_files():
    try:
        statistics_main()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=e
        )