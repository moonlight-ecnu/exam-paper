# Frontend Refinement & Feature Completion Plan

The user wants a complete and working frontend flow.
Current status:
- Login works (verified).
- Page doesn't switch after login (Need to fix `showMainPage` visibility toggle).
- Missing specific UI requirements:
    1. "Enter Invite Code" UI.
    2. Group Space: Member List, File List, Upload/Download.
    3. Generated HTML preview (User wants to "open" the downloaded HTML).

## 1. Fix Navigation Flow
*   **Issue**: Login success toast appears but page doesn't switch.
*   **Fix**: Verify `app.showMainPage()` logic in `js/app.js`. Ensure CSS classes (`hidden`) are correctly applied.

## 2. Enhance Group Space UI (`frontend/index.html` & `js/app.js`)
*   **Member List**: The `GroupInfo` DTO in backend includes `members` (a dict of user_id -> role).
    *   *Backend Check*: Does `GroupInfo` return detailed member info (names) or just IDs?
    *   *Refinement*: If it only returns IDs, we might need a `get_group_detail` API or `batch_get_users`. For MVP, we'll list IDs or update `GroupInfo` to include cached names if possible (or just show "Member [ID]").
    *   *Frontend*: Add a "Members" section in the Group Detail view.
*   **Invite Code Interface**:
    *   Currently, "Join Group" modal exists. Ensure it clearly says "Enter Invite Code" (which is the Group ID in this system).
*   **File Space**:
    *   Existing file list is okay. Ensure "Upload" and "Download" buttons are intuitive.

## 3. Generated File Preview
*   **Requirement**: "Download to generated file (html) and open page".
*   **Current**: It opens the signed COS URL in a new tab.
*   **Refinement**: This is actually correct behavior for a web app (browser opens HTML). I will ensure the button explicitly says "Preview/Open".

## 4. Backend Adjustments (if needed)
*   **Member Details**: Check `GroupInfo` in `backend/application/dto/group_info.py`.
    *   If it only has IDs, the frontend user experience is poor.
    *   *Action*: Update `GroupInfo` to fetch user names from User collection (using `User.objects.in_bulk` or similar).

## Execution Steps
1.  **Backend Analysis**: Check `GroupInfo` content. Update if necessary to include member names.
2.  **Frontend Fixes**:
    *   Fix Login -> Main Page transition (CSS/JS).
    *   Update "Join Group" UI to emphasize "Invite Code".
    *   Add "Member List" sidebar/section in Group Detail view.
    *   Ensure "AI Generated File" opens in new tab (Preview).
3.  **Verification**: Test the full flow.

