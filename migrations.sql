Conexão DB: mysql://root:1234@localhost:3306/meudb
CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> 608e1fabc776

INSERT INTO alembic_version (version_num) VALUES ('608e1fabc776');

-- Running upgrade 608e1fabc776 -> 3ffb3ba0e35c

CREATE TABLE applications (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    name VARCHAR(120) NOT NULL, 
    acronym VARCHAR(5) NOT NULL, 
    creation_date DATETIME NOT NULL, 
    PRIMARY KEY (id)
);

CREATE TABLE users (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    name VARCHAR(120) NOT NULL, 
    username VARCHAR(20) NOT NULL, 
    password VARCHAR(100) NOT NULL, 
    email VARCHAR(120) NOT NULL, 
    is_locked_out BOOL NOT NULL, 
    failed_pass_att_count INTEGER NOT NULL, 
    creation_date DATETIME NOT NULL, 
    last_login_date DATETIME, 
    last_change DATETIME, 
    temporary_password VARCHAR(100), 
    temporary_password_expiration DATETIME, 
    PRIMARY KEY (id)
);

CREATE TABLE roles (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    name VARCHAR(120) NOT NULL, 
    application_id INTEGER NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(application_id) REFERENCES applications (id)
);

CREATE TABLE user_role (
    user_id INTEGER, 
    role_id INTEGER, 
    FOREIGN KEY(role_id) REFERENCES roles (id), 
    FOREIGN KEY(user_id) REFERENCES users (id)
);

UPDATE alembic_version SET version_num='3ffb3ba0e35c' WHERE alembic_version.version_num = '608e1fabc776';

-- Running upgrade 3ffb3ba0e35c -> 3d5df7171b66

CREATE TABLE tasks (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    name VARCHAR(120) NOT NULL, 
    tag_name VARCHAR(20) NOT NULL, 
    icon VARCHAR(255), 
    show_in_menu INTEGER, 
    menu_title VARCHAR(255), 
    PRIMARY KEY (id)
);

UPDATE alembic_version SET version_num='3d5df7171b66' WHERE alembic_version.version_num = '3ffb3ba0e35c';

-- Running upgrade 3d5df7171b66 -> b05b6e3557e8

CREATE TABLE actions (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    name VARCHAR(120) NOT NULL, 
    task_id INTEGER NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(task_id) REFERENCES tasks (id)
);

UPDATE alembic_version SET version_num='b05b6e3557e8' WHERE alembic_version.version_num = '3d5df7171b66';

-- Running upgrade b05b6e3557e8 -> d3ededb8ce83

CREATE TABLE role_action (
    role_id INTEGER, 
    action_id INTEGER, 
    FOREIGN KEY(action_id) REFERENCES actions (id), 
    FOREIGN KEY(role_id) REFERENCES roles (id)
);

UPDATE alembic_version SET version_num='d3ededb8ce83' WHERE alembic_version.version_num = 'b05b6e3557e8';

-- Running upgrade d3ededb8ce83 -> 49e6183425c3

CREATE OR REPLACE VIEW user_permissions AS
        SELECT tasks.tag_name, actions.name AS action_name, users.username, applications.acronym,
               tasks.id AS task_id, roles.id AS role_id, actions.id AS action_id, users.id AS user_id,
               tasks.name AS task_name, roles.name AS role_name, users.name
        FROM actions
        JOIN tasks ON actions.task_id = tasks.id
        JOIN role_action ON actions.id = role_action.action_id
        JOIN roles ON role_action.role_id = roles.id
        JOIN applications ON roles.application_id = applications.id
        JOIN user_role ON roles.id = user_role.role_id
        JOIN users ON user_role.user_id = users.id;

UPDATE alembic_version SET version_num='49e6183425c3' WHERE alembic_version.version_num = 'd3ededb8ce83';

-- Running upgrade 49e6183425c3 -> 69382a0c5998

ALTER TABLE roles ADD CONSTRAINT uq_roles_name_application_id UNIQUE (name, application_id);

UPDATE alembic_version SET version_num='69382a0c5998' WHERE alembic_version.version_num = '49e6183425c3';

-- Running upgrade 69382a0c5998 -> 8f36ed25393d

ALTER TABLE users ADD CONSTRAINT uq_roles_email UNIQUE (email);

ALTER TABLE users ADD CONSTRAINT uq_roles_username UNIQUE (username);

UPDATE alembic_version SET version_num='8f36ed25393d' WHERE alembic_version.version_num = '69382a0c5998';

