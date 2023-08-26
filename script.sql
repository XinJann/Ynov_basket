CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    cookie TEXT
);

CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    player_id INTEGER NOT NULL,
    first_name TEXT NOT NULL,
    height_feet INTEGER,
    height_inches INTEGER,
    last_name TEXT NOT NULL,
    position TEXT NOT NULL,
    team_id INTEGER NOT NULL,
    weight_pounds INTEGER
);

CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    team_id INTEGER NOT NULL,
    abbreviation TEXT NOT NULL,
    city TEXT NOT NULL,
    conference TEXT NOT NULL,
    division TEXT NOT NULL,
    full_name TEXT NOT NULL,
    team_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    game_id INTEGER NOT NULL,
    game_date TEXT NOT NULL,
    home_team_id INTEGER NOT NULL,
    home_team_score INTEGER NOT NULL,
    periode INTEGER NOT NULL,
    postseason BOOLEAN NOT NULL,
    season INTEGER NOT NULL,
    game_status TEXT NOT NULL,
    game_time TEXT,
    visitor_team_id INTEGER NOT NULL,
    visitor_team_score INTEGER NOT NULL
);