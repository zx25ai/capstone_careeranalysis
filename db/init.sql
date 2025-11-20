CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name TEXT,
  email TEXT UNIQUE,
  summary TEXT,
  education JSONB,
  coursework JSONB,
  skills JSONB
);

CREATE TABLE job_roles (
  id SERIAL PRIMARY KEY,
  title TEXT,
  description TEXT,
  required_skills JSONB,
  seniority TEXT
);

INSERT INTO job_roles (title, description, required_skills, seniority)
VALUES
('Data Scientist', 'Build ML models', '["python","pandas","ml","statistics"]', 'mid'),
('Product Manager', 'Lead product strategy', '["product management","roadmapping","stakeholder mgmt"]', 'senior'),
('Data Engineer', 'Build ETL pipelines', '["sql","airflow","spark","python"]', 'mid');
