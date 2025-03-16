-- Insertion de l'administrateur
INSERT INTO users (
    id,
    first_name,
    last_name,
    email,
    password,
    is_admin
) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    -- Hash du mot de passe 'admin1234' généré avec bcrypt2
    '$2a$12$RWH8y0WgWnrC7YrPQvVJ1eDgx0hcGNHJHFeq1gTK17IFGlWLcXsT6',
    TRUE
);

-- Insertion des équipements initiaux
INSERT INTO amenities (
    id,
    name
) VALUES 
    ('550e8400-e29b-41d4-a716-446655440000', 'WiFi'),
    ('6ba7b810-9dad-11d1-80b4-00c04fd430c8', 'Swimming Pool'),
    ('6ba7b811-9dad-11d1-80b4-00c04fd430c8', 'Air Conditioning');