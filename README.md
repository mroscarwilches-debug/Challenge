# Challenge
Welcome to the challenge series for practicing confidence and Git skills.

## Getting started

- `GIT_WORKFLOW_GUIDELINES.md` – branch naming, commit messages, and PR structure.
- `GYM_PYTHON_LESSONS.md` – project plan and lesson structure for gym-themed Python exercises.
- `codigo/kg_to_lb_challenge.py` – first Python challenge: convert kilograms to pounds.

Markdown

# Project Structure & Database Configuration

This repository contains the basic architecture of the project. We use Docker to run all the services in a local environment.

## System Architecture

This diagram shows the structure of the app. It explains how the Frontend, the API, and the Database communicate with each other:

<img width="685" height="378" alt="WhatsApp Image 2026-05-13 at 9 55 03 PM" src="https://github.com/user-attachments/assets/e222947f-9a1b-4014-97ce-dad0d5a662f5" />

---

## Components

### 1. Database Instance in Docker
Configured and deployed a **PostgreSQL** database using a Docker container.

* **Database Engine:** PostgreSQL
* **Local Port:** 5432
* **Management:** Connected to the API and Frontend using Docker Compose.

### 2. Database Connection in DBeaver
To manage the database, see the tables and run SQL queries, we connected the container to **DBeaver**, connection succefull!
