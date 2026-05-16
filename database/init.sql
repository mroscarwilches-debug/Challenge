# Database initialization script for the gym-app
CREATE TABLE public.users (
    id bigint NOT NULL,
    "name" varchar NOT NULL,
    weight_kg decimal NOT NULL,
    created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT users_pk PRIMARY KEY (id)
);