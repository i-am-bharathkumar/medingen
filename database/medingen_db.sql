-- Create database
CREATE DATABASE IF NOT EXISTS medingen;
USE medingen;

-- Create users table for authentication
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create medicines table
CREATE TABLE IF NOT EXISTS medicines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    salt_content VARCHAR(100),
    uses TEXT,
    how_it_works TEXT,
    price DECIMAL(10, 2),
    manufacturer VARCHAR(100),
    is_featured BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create medicine_details table
CREATE TABLE IF NOT EXISTS medicine_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    medicine_id INT,
    usage_instructions TEXT,
    side_effects TEXT,
    precautions TEXT,
    storage_instructions TEXT,
    FOREIGN KEY (medicine_id) REFERENCES medicines(id)
);

-- Create generic_alternatives table
CREATE TABLE IF NOT EXISTS generic_alternatives (
    id INT AUTO_INCREMENT PRIMARY KEY,
    medicine_id INT,
    name VARCHAR(100) NOT NULL,
    manufacturer VARCHAR(100),
    price DECIMAL(10, 2),
    salt_content VARCHAR(100),
    availability VARCHAR(50),
    FOREIGN KEY (medicine_id) REFERENCES medicines(id)
);

-- Create comparisons table
CREATE TABLE IF NOT EXISTS comparisons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    medicine_id INT,
    title VARCHAR(100),
    price DECIMAL(10, 2),
    original_price DECIMAL(10, 2),
    discount VARCHAR(20),
    chemical_formulation VARCHAR(100),
    rating DECIMAL(3, 1),
    FOREIGN KEY (medicine_id) REFERENCES medicines(id)
);

-- Create reviews table
CREATE TABLE IF NOT EXISTS reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    medicine_id INT,
    rating INT,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (medicine_id) REFERENCES medicines(id)
);

-- Create faqs table
CREATE TABLE IF NOT EXISTS faqs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    medicine_id INT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    FOREIGN KEY (medicine_id) REFERENCES medicines(id)
);

-- Insert sample data

-- Insert users
INSERT INTO users (username, password) VALUES
('admin', 'admin123'), -- In a real app, this would be hashed
('user', 'user123');

-- Insert medicine data for UDILIV 300MG
INSERT INTO medicines (name, description, salt_content, uses, how_it_works, price, manufacturer, is_featured) VALUES
('UDILIV 300MG TABLET 10''S', 'UDILIV 300MG TABLET 10''S contains Ursodeoxycholic Acid, which belongs to the class of medications called gallstone dissolution agents. It has been used for several decades as a therapeutic agent to manage various liver disorders. UDCA is primarily used to treat gallstone disease when the gallstones primarily consist of cholesterol and the treatment of primary biliary cholangitis (PBC), a rare autoimmune liver disease. UDCA works by reducing cholesterol absorption, improving bile flow, and exerting anti-inflammatory effects, thereby promoting liver health.', 'Ursodeoxycholic Acid', '- Helps in dissolving gallstones\n- Used in the treatment of primary biliary cholangitis (PBC)\n- Aids in managing other cholestatic liver disorders\n- Assists in improving liver function\n- Helps in improving liver function', 'How UDILIV 300MG TABLET 10''S Works\n\nPrimarily, UDILIV 300MG TABLET 10''S is primarily designed as a gallstone dissolution agent to reduce the cholesterol content and weight and the specific liver disorders being treated. It is typically prescribed by a pediatrician or gastroenterologist who will determine the appropriate dosage.\n\nWhen used in a therapeutic context, UDILIV 300MG TABLET 10''S for adults varies depending on the specific condition being treated. For instance, if it''s being used to dissolve gallstones, the dosage may vary from 8 to 10 mg/kg/day. In the treatment of primary biliary cholangitis (PBC), the typical dose ranges from 13-15 mg/kg/body weight per day, also divided into multiple doses. However, dosages may differ based on individual factors including age, weight, health condition, and as directed by your healthcare professional.', 149.00, 'Abbot India Ltd', TRUE);

-- Insert medicine details for UDILIV 300MG
INSERT INTO medicine_details (medicine_id, usage_instructions, side_effects, precautions, storage_instructions) VALUES
(1, 'Take as directed by your doctor.', '- Diarrhea\n- Abdominal discomfort\n- Nausea\n- Itching\n- Hair loss (rare)', 'Consult your doctor before use if you have any pre-existing conditions.', 'Store in a cool, dry place away from direct sunlight.');

-- Insert generic alternatives for UDILIV 300MG
INSERT INTO generic_alternatives (medicine_id, name, manufacturer, price, salt_content, availability) VALUES
(1, 'URSOCOL PLUS TAB', 'Sun Pharma', 120.00, 'Ursodeoxycholic Acid', 'In Stock'),
(1, 'UDICHOL 300MG TAB', 'Lupin Ltd', 125.00, 'Ursodeoxycholic Acid', 'In Stock'),
(1, 'UDILIV 150 TABLET', 'Abbot India Ltd', 75.00, 'Ursodeoxycholic Acid', 'In Stock');

-- Insert comparison data
INSERT INTO comparisons (medicine_id, title, price, original_price, discount, chemical_formulation, rating) VALUES
(1, 'Dolo 650 mg', 34.00, 36.00, '5% OFF', 'PARACETAMOL', 4.5),
(1, 'Dolo 650 mg', 34.00, 36.00, '5% OFF', 'PARACETAMOL', 4.5),
(1, 'Dolo 650 mg', 34.00, 36.00, '5% OFF', 'PARACETAMOL', 4.7),
(1, 'Dolo 650 mg', 34.00, 36.00, '5% OFF', 'PARACETAMOL', 4.9);

-- Insert reviews
INSERT INTO reviews (medicine_id, rating, comment) VALUES
(1, 5, 'The medicine is good it is bit costly when compared with the exact generic medicine'),
(1, 4, 'The medicine is good it is bit costly when compared with the exact generic medicine'),
(1, 3, 'The medicine is good it is bit costly when compared with the exact generic medicine'),
(1, 5, 'The medicine is good it is bit costly when compared with the exact generic medicine');

-- Insert FAQs for Paracetamol
INSERT INTO faqs (medicine_id, question, answer) VALUES
(1, 'How long after taking Paracetamol?', 'Paracetamol usually starts working within 30 minutes after taking a dose of Paracetamol tablets or syrup, relieves the same dose again. If you aren''t better 30 minutes of a dose, you do not need to take another one until the next standard dose.'),
(1, 'Is it OK to take 2 paracetamol every 4 hours?', 'The usual dose for adults is one or two 500mg tablets up to 4 times in 24 hours. Always leave at least 4 hours between doses. Do not take paracetamol for more than 3 days without talking to your doctor.'),
(1, 'Is Paracetamol safe for long term use?', 'Paracetamol is an effective treatment for mild to moderate pain and fever in adults and children, when used as directed in product information. The drug has been widely used for decades in many products and is safe when used correctly according to the label.'),
(1, 'Is Paracetamol safe for children?', 'Paracetamol is considered safe for children over the age of 2 months when used as directed by the doctor. Always follow the dosage instructions provided and never exceed the recommended dose.'),
(1, 'Can I take Paracetamol while pregnant?', 'Paracetamol is generally considered safe during pregnancy when used as directed. However, always consult your doctor before taking any medication during pregnancy.'),
(1, 'Can I take Paracetamol and Ibuprofen together?', 'Yes, taking paracetamol and ibuprofen together is safe when done correctly. They are different types of pain-relieving medicine. If needed, most people can take both paracetamol and ibuprofen together if you are over 16.'),
(1, 'Should I avoid alcohol while taking Paracetamol?', 'It''s usually safe to drink alcohol while using paracetamol. However, if you''re using it regularly or at the highest doses, consult your doctor if you are not sure.'),
(1, 'What are the serious side effects of taking Paracetamol?', 'Paracetamol rarely causes side effects when taken as directed. However, if you experience any serious side effects, it is advised to stop this medicine for the duration suggested by the doctor. Consult your doctor if you experience any bothersome side effects.');