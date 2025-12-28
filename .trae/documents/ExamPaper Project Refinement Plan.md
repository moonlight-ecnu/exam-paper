# Project Refinement Plan

## 1. Environment & Configuration
1.  **Create `requirements.txt`**: Add necessary dependencies (`Flask`, `mongoengine`, `redis`, `qcloud-cos-python`, `requests`, `PyYAML`).
2.  **Implement Config Loader**: 
    -   Modify `backend/infra/config/config.py` to read `etc/config.yaml`.
    -   Load configuration into environment variables or a global config object so that other modules (COS, OpenAI) can access them without hardcoding.
    -   Ensure `init_app` in `config.py` calls this loader.

## 2. Infrastructure Layer Refinement
### COS Integration (`backend/infra/storage/cos.py`)
1.  **Remove Hardcoding**: Replace hardcoded `Bucket`, `SecretId`, `SecretKey` with values loaded from config.
2.  **Fix Bugs**: Correct `gen_signed_url` to use `self.client` instead of `cos_client.client`.
3.  **Enhance**: Ensure `upload_from_fp` is robust.

### OpenAI/Model Integration (`backend/infra/util/completion.py`)
1.  **Config Usage**: Update `parser_base64_img` to use the API key from the loaded configuration.
2.  **Optimization**: Ensure the function can handle the file input efficiently (e.g., from memory buffer).

## 3. Service Layer Implementation (`backend/application/service/group.py`)
### Complete `upload` function
1.  **Parameter Handling**: Update to accept file objects and form data correctly.
2.  **Origin File Processing**:
    -   Upload original file to COS using `cos_client.upload_from_fp`.
    -   Create and save `File` entity to MongoDB.
3.  **Generation Processing**:
    -   Call `completion.parser_base64_img` with the uploaded image.
    -   Save the generated HTML content to a temporary file or memory buffer.
    -   Upload the generated HTML file to COS.
    -   Create and save `GenFile` entity to MongoDB.
4.  **Error Handling**: Add try-catch blocks to handle COS or DB failures.

## 4. Controller Layer Adjustment (`backend/adaptor/controller/group.py`)
1.  **Upload Endpoint**: Update `upload` route to extract metadata from `request.form` and file from `request.files` (since it's a multipart request), instead of `request.get_json()`.

## 5. Documentation & Frontend
1.  **API Documentation**: Create `API_DOCS.md` detailing endpoints (especially `upload`, `download`, `create_group`, `join_group`), parameters, and response formats.
2.  **Minimal Frontend**: Create `frontend/index.html` to demonstrate:
    -   User Login (mock/simple).
    -   Group Management (Create/Join).
    -   File Upload (Multipart form).
    -   File List & Download.
