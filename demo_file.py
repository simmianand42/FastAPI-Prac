from fastapi import File, FastAPI, UploadFile
import shutil

app = FastAPI()

@app.post('/file')
def get_file(file: bytes = File()):
    content = file.decode('utf-8')
    lines = content.split('\n')
    return {'lines: ': lines}

@app.post('/uploadfile')
def get_uploadfile(file: UploadFile = File(...)):
    path = f"files/{file.filename}"
    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return {
        'filename': path,
        'type': file.content_type
    }

