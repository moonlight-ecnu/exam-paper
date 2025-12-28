# API Documentation

## Group Management

### Create Group
- **URL**: `/group/create`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Header**: `Authorization: <JWT_TOKEN>`
- **Body**:
  ```json
  {
    "name": "Group Name"
  }
  ```
- **Response**:
  ```json
  {
    "code": 200,
    "msg": "success",
    "data": {
      "group_id": "...",
      "name": "Group Name",
      ...
    }
  }
  ```

### Invite User
- **URL**: `/group/invite`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Header**: `Authorization: <JWT_TOKEN>`
- **Body**:
  ```json
  {
    "group_id": "...",
    "user_email": "user@example.com"
  }
  ```
- **Response**: Success message.

### Join Group
- **URL**: `/group/join`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Header**: `Authorization: <JWT_TOKEN>`
- **Body**:
  ```json
  {
    "group_id": "..."
  }
  ```
- **Response**: Group Info.

### Upload File
- **URL**: `/group/upload`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Header**: `Authorization: <JWT_TOKEN>`
- **Form Fields**:
  - `file`: (File Object) The file to upload.
  - `group_id`: (String) Group ID.
  - `subject`: (String) Subject (e.g., Math, English).
  - `year`: (String, Optional) Year.
  - `paper_type`: (String) `contest`, `exam`, or `exercise`.
  - `exam_type`: (String, Optional) `monthly`, `mid`, `final` (Required if paper_type is exam).
  - `description`: (String, Optional) Description.
- **Response**:
  ```json
  {
    "code": 200,
    "msg": "success",
    "data": {
      "file_id": "...",
      "filename": "...",
      "url": "https://cos-url...",
      "meta_info": { ... }
    }
  }
  ```

### Download File
- **URL**: `/group/download`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Header**: `Authorization: <JWT_TOKEN>`
- **Body**:
  ```json
  {
    "group_id": "...",
    "file_id": "...",
    "target_type": "origin" or "gen"
  }
  ```
- **Response**:
  ```json
  {
    "code": 200,
    "msg": "success",
    "data": {
      "file_id": "...",
      "url": "https://signed-cos-url...",
      ...
    }
  }
  ```
