# from fastapi import FastAPI, HTTPException

# app = FastAPI()

# @app.get("/user/{id}")
# def get_user(id: int):
#     if id == 1:
#         return {
#             "id": 1,
#             "name": "Shraddha"
#         }

#     raise HTTPException(
#         status_code=404,
#         detail="User not found"
#     )



# from fastapi import FastAPI, UploadFile, File, HTTPException

# app = FastAPI()

# @app.post("/extract-document")
# async def extract_document(file: UploadFile = File(...)):

#     if file.content_type != "application/pdf":
#         raise HTTPException(
#             status_code=400,
#             detail="Only PDF files are allowed."
#         )

#     # Simulate document extraction
#     extracted_text = "Invoice Number: INV-101\nAmount: ₹15,000"

#     return {
#         "filename": file.filename,
#         "status": "success",
#         "extracted_text": extracted_text
#     }





from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.post("/extract")
async def extract_document(file: UploadFile = File(...)):

    # Step 1
    text = extract_text(file)

    # Step 2
    prompt = f"""
    Extract:
    - Name
    - PAN
    - Aadhaar Number
    - Date of Birth

    Document:
    {text}
    """

    # Step 3
    result = llm.invoke(prompt)

    # Step 4
    return result