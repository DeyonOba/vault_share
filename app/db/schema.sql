-- Author: Gideon Oba
-- Render Schema using the web app <Eraser>
-- LINK: https://app.eraser.io
-- Ensure you replace comments "--" with "//" when rendering the schema

users [icon: user, color: blue] {
  id string pk
  username string unique not null
  email string unique not null
  password string not null
  role string default user
  memory_allocated float default 0  
  memory_used float default 0
  createdAt timestamp default current_timestamp
}

workspaces [icon: home] {
  id string pk
  name string not null
  admin_id string
  total_memory float default 10
  memory_used float default 0
  max_users int default 5
  createdAt timestamp default current_timestamp
  updatedAt timestamp default current_timestamp
}

workspace_users [icon: users, color: blue] {
  id string pk
  workspace_id string
  user_id string
  role string not null
  memory_allocated float default 0
  createdAt timestamp default current_timestamp
}

folders [icon: folder] {
  id string pk
  name string not null
  workspace_id string
  user_id string
  parent_folder_id string null
  is_root boolean default
  createdAt timestamp default current_timestamp
}

files [icon: file, color: black] {
  id string pk
  name string not null
  path string not null
  workspace_id string
  user_id string
  folder_id string
  size float not null
  is_directory boolean default false
  createdAt timestamp default current_timestamp
  updatedAt timestamp default current_timestamp
}

invites [icon: mail, color: green] {
  id string pk
  invite_type string not null
  workspace_id string
  inviter_id string
  invitee_email string not null
  status string default pending
  createdAt timestamp default current_timestamp
}

alerts [icon: bell, color: red] {
  id string pk
  alert_type string not null
  user_id string
  workspace_id string
  message string not null
  is_read boolean default false
  createdAt timestamp default current_timestamp
}

workspace_users.workspace_id > workspaces.id 
workspace_users.user_id > users.id

workspaces.admin_id > users.id

folders.workspace_id > workspaces.id
folders.user_id > users.id
folders.parent_folder_id > folders.id

files.folder_id > folders.id
files.user_id > users.id
files.workspace_id > workspaces.id

invites.workspace_id > workspaces.id
invites.inviter_id > users.id

alerts.user_id > users.id
alerts.workspace_id > workspaces.id