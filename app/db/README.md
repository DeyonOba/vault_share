# Database Documentation

## Schema description

### `User`
Represents users of the system with their roles, memory usage, and allocations.

### Workspace
Represents a workspace, including memory usage, maximum users, and admin.

### WorkspaceUser
Manages the relationship between users and workspaces, including their roles and allocated memory.

### Folder
Represents folders, which can be nested and belong to either users or admins in a workspace.

### File
Represents files within the workspace, stored in folders, with details such as size and ownership.

### Invite
Tracks invitations sent by admins to users, including the status of the invite (pending, accepted, declined).

### Alert
A system that notifies users about events like memory usage warnings, invites, and more.
