# Database Documentation

For this project, I will use an SQLite database due to its simplicity in testing and integration with Python and GitHub actions.

## Database ERD
![db_erd](../../images/db_schema.png)

## Schema description
### `User`: *Table Name -> `users`*
Represents users of the system with their roles, memory usage, and allocations.
*
|ColumnName|DataType|Constraints|Description|
|:--|:--|:--|:--|
|`id`|`String`|`pk`| User identification number, primary key of users table|
|`username`|`String`|`unique` `not null`| User name of the user should be unique and filled in upon account registration.|
|`email`|`String`|`unique` `not null`| User email is unique and filled in upon account registration, just like the user name.|
|`password`|`String`| `not null`| The Password to the user's account, must be filled in upon account registration.|
|`role`|`String`|`default="user"`| Team role of the user, defaults to "user", but "admin" could also be assigned.|
|`memory_allocation`| `Float`|`default=0`|Memory quota assigned by admin to user's in MB.|
|`memory_used`|`Float`|`default=0`| Memory currently used in MB|
|`createdAt`| `DateTime`|`default=0`| Stores the time the account is created.|
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
