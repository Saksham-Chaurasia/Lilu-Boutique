
create database if not exists boutique;
use boutique;

CREATE TABLE IF NOT EXISTS customer_data (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    dates DATE,
    name VARCHAR(255),
    phone VARCHAR(255),
    email VARCHAR(255),
    delivery_date DATE,
    category VARCHAR(255),
    registration_date DATE DEFAULT (CURRENT_DATE()),
    status ENUM('ordered', 'delivered', 'cancelled', 'overdue','extended') DEFAULT 'ordered'
);



CREATE TABLE IF NOT EXISTS blouse_data (
    blouse_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    blouse_full_length float,
    shoulder float,
    hand_length float,
    hand_rounding float, 
    arm_hole float,
    upper_chest float,
    chest float,
    waist float,
    front_neck_deep float,
    back_neck_deep float,
    boat_neck float,
    collar float,
    preferred_neck_style varchar(255),
    preferred_blouse_style varchar(255),
    closingwith varchar(255),
    padding varchar(255),
    piping varchar(255),
    lace varchar(255),
    tassels varchar(255),
    comments text,
    FOREIGN KEY (customer_id) REFERENCES customer_data(customer_id)
   
);

CREATE TABLE IF NOT EXISTS blouse_files (
    bfile_id INT AUTO_INCREMENT PRIMARY KEY,
    blouse_id INT,
    file_data LONGBLOB,
    file_name VARCHAR(255),
    FOREIGN KEY (blouse_id) REFERENCES blouse_data(blouse_id)
);

CREATE TABLE IF NOT EXISTS topbottom_data (
    topbottom_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    top_full_length float,
    shoulder float,
    hand_length float,
    hand_rounding float, 
    arm_hole float,
    upper_chest float,
    chest float,
    top_waist float,
    front_neck_deep float,
    back_neck_deep float,
    boat_neck float,
    collar float,
    side_cuts float,
    hip float,
    bottom_full_length float,
    leg_rounding float,
    thigh_rounding float,
    bottom_waist float,
    bottom_style varchar(255),
    comments text,
    FOREIGN KEY (customer_id) REFERENCES customer_data(customer_id)
   
);

CREATE TABLE IF NOT EXISTS topbottom_files (
    tbfile_id INT AUTO_INCREMENT PRIMARY KEY,
    topbottom_id INT,
    file_data LONGBLOB,
    file_name VARCHAR(255),
    FOREIGN KEY (topbottom_id) REFERENCES topbottom_data(topbottom_id)
);

CREATE TABLE IF NOT EXISTS blehenga_data (
    blehenga_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    blouse_id INT,
    lehenga_full_length FLOAT,
    waist_rounding FLOAT,
    hip_around FLOAT,
    frock_full_length FLOAT,
    FOREIGN KEY (customer_id) REFERENCES customer_data(customer_id),
    FOREIGN KEY (blouse_id) REFERENCES blouse_data(blouse_id)
);




CREATE TABLE IF NOT EXISTS boys_data (
    boys_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    full_length float,
    hand_length float,
    collar float,
    shoulder float,
    side_cuts float,
    pant_length float, 
    thigh_rounding float,
    leg_rounding float,
    pant_style varchar(255),
    comments text,
    FOREIGN KEY (customer_id) REFERENCES customer_data(customer_id)
   
);

CREATE TABLE IF NOT EXISTS boys_files (
    bbfile_id INT AUTO_INCREMENT PRIMARY KEY,
    boys_id INT,
    file_data LONGBLOB,
    file_name VARCHAR(255),
    FOREIGN KEY (boys_id) REFERENCES boys_data(boys_id)
);



CREATE TABLE IF NOT EXISTS maggam_data (
    maggam_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    blouse_id INT,
    comments TEXT,
    maggam_description VARCHAR(255),
    FOREIGN KEY (customer_id) REFERENCES customer_data(customer_id),
    FOREIGN KEY (blouse_id) REFERENCES blouse_data(blouse_id)
);


CREATE TABLE IF NOT EXISTS maggam_files (
    mfile_id INT AUTO_INCREMENT PRIMARY KEY,
    maggam_id INT,
    file_data LONGBLOB,
    file_name VARCHAR(255),
    FOREIGN KEY (maggam_id) REFERENCES maggam_data(maggam_id)
);


CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);


