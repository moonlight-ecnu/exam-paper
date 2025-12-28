# Frontend Refinement Plan

The user wants a complete frontend implementation, not just the login page.
Current state: The `frontend/index.html` file *already contains* the full implementation (Login, Group Management, File Upload/Download) as per the previous tool output. However, the user's message suggests they might be perceiving it as incomplete, or perhaps they want a more structured/split codebase (HTML/CSS/JS separated) or simply want to ensure the logic connects correctly to port 5000.
Also, I need to ensure the frontend code explicitly points to `http://127.0.0.1:5000` for API calls, which it already does (`const BASE_URL = 'http://127.0.0.1:5000';`), but I will double-check and perhaps verify if CORS is an issue since the frontend is served on 8000 and backend on 5000.

Steps:
1.  **Verify CORS**: Since frontend (8000) and backend (5000) are on different ports, browsers will block requests unless the backend sends CORS headers. I need to add `flask-cors` to the backend.
2.  **Refactor Frontend**: Although a single HTML file works, splitting it into `index.html`, `style.css`, and `app.js` is better practice and might be what the user means by "complete code". I will split the files.
3.  **Enhance Frontend Features**: Ensure all "complete" features are present and obvious:
    *   **Dashboard**: Show joined groups list (Mock or implement list API if missing).
    *   **File List**: Show files in a group (Need `list_files` API on backend or mock it for now if API is missing).
    *   **Upload/Download**: Already there, but can be polished.
4.  **Backend Adjustments**:
    *   Install and configure `flask-cors`.
    *   Implement `list_groups` and `list_files` APIs if they are missing/empty in the backend, so the frontend has something to show in the "complete" interface.

## Plan Detail:

### 1. Backend: Add CORS and List APIs
*   **Install `flask-cors`**: Add to `requirements.txt` and `app.py`.
*   **Implement `list_files`**: The `backend/application/service/group.py` has an empty `list_files`. I need to implement it to query MongoDB for files in a group.
*   **Implement `my_groups`**: Add an endpoint to list groups the user belongs to, so the dashboard isn't empty.

### 2. Frontend: Refactor & Complete
*   **Split Files**:
    *   `frontend/index.html`: Structure only.
    *   `frontend/css/style.css`: Styles.
    *   `frontend/js/api.js`: API wrapper.
    *   `frontend/js/main.js`: UI Logic.
*   **UI Flow**:
    *   Login -> Dashboard (List of Groups).
    *   Click Group -> Group Detail (List of Files + Upload Button).
    *   File Item -> Download Origin / Download Generated.

### 3. Execution Order
1.  Update `requirements.txt` with `flask-cors`.
2.  Update `app.py` to enable CORS.
3.  Implement `list_files` in `backend/application/service/group.py` and controller.
4.  Implement `my_groups` in `backend/application/service/user.py` (or group service) and controller.
5.  Refactor frontend into `index.html`, `css/style.css`, `js/app.js`.
6.  Restart frontend server.
