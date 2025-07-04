CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    gender ENUM('male', 'female') NOT NULL,
    birthday DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS recipes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    under ENUM('yes', 'no') NOT NULL,
    posted_by VARCHAR(100) NOT NULL,
    users_id INT NOT NULL,
    description VARCHAR(255) NOT NULL,
    instruction VARCHAR(160) NOT NULL,
    date_cooked DATE NOT NULL,
    FOREIGN KEY (users_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_recipes_users_id ON recipes(users_id); 