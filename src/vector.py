from configs.config import CLIENT
from pathlib import Path
from typing import Any


def create_vector_store(store_name: str) -> dict[str, Any]:
    # NOTE: chunking strategy : https://platform.openai.com/docs/api-reference/vector-stores
    vector_store = CLIENT.vector_stores.create(name=store_name)
    return {
        "vector_store_id": vector_store.id,
        "vector_store_name": vector_store.name,
        "created_at": vector_store.created_at,
        "file_count": vector_store.file_counts.completed,
    }


# Individual files can be up to 512 MB, and the size of all files uploaded by one organization
# can be up to 100 GB.
def upload_pdf_to_vector_store(pdf_filepath: Path, vector_store_id: str):
    file_name = pdf_filepath.stem
    try:
        file_response = CLIENT.files.create(
            file=pdf_filepath.open("rb"), purpose="assistants"
        )
        _ = CLIENT.vector_stores.files.create(
            vector_store_id=vector_store_id, file_id=file_response.id
        )
        return {"file": file_name, "file_id": file_response.id, "status": "success"}

    except Exception as e:
        print(
            f"Error occured while uploading file with name {file_name} to the vector store {e}"
        )
        return {"file": file_name, "status": "failed", "error": e}
