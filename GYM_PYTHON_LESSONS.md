# Gym Python Lessons and Project Plan

This document defines the learning path for the gym platform project. The goal is to start with small Python challenges and grow toward infrastructure, Docker, services, and a gym app.

## 1. Project Vision

Create a small platform for gym-related tools and utilities.

Initial goals:
- Practice Git workflows and PR collaboration
- Learn Python logic with simple scripts
- Explore infrastructure concepts later
- Add Docker and service-based components as the project grows

## 2. Learning Topics

### 2.1 Logic and Python basics
- Variables, data types, arithmetic, and control flow
- Functions and reusable code
- Input/output interaction in scripts
- Small calculators and converters for gym use

### 2.2 Infrastructure concepts
- What is infrastructure?
- The role of servers, containers, and deployment
- Basic architecture for a small app
- Environment setup and dependencies

### 2.3 Docker and containers
- What is Docker and why use it?
- Containerizing a Python app
- Building and running Docker images
- Docker Compose for multi-service setups

### 2.4 Services and APIs
- What is a service?
- How services communicate
- Simple API design and endpoints
- Building a small backend for the gym app

### 2.5 Gym app ideas
- Workout calculator utilities
- Nutrition helpers and conversion tools
- Simple user progress logging
- Exercise library or plan manager

## 3. Structure for the lesson series

### Phase 1: Python challenges
- Start with small command-line scripts
- Keep the problems short and practical
- Focus on logic and correctness

### Phase 2: Build a small app
- Combine several utilities into a simple project
- Add structure, modules, and reusable code
- Introduce basic tests

### Phase 3: Infrastructure and Docker
- Add Docker support for the app
- Learn how to run the project in a container
- Discuss deployment concepts

### Phase 4: Services
- Create a service for a gym tool or API
- Explore request/response flow
- Add a simple frontend or API consumer if needed

## 4. Initial Python challenge list

1. Convert kilograms to pounds
2. Calculate BMI from weight and height
3. Compute workout volume from sets, reps, and weight
4. Convert calories or macros for gym meals
5. Track simple progress with JSON or CSV data

## 5. How we will use these documents

- Create branches with `feature/` or `doc/`
- Write code in small steps and open PRs
- Use this guide to name branches, commits, and PRs
- Review each challenge together and merge when ready

## 6. First challenge: Gym unit converter

Create a Python script that:
- asks for a weight value in kilograms
- converts the value to pounds
- prints the result clearly

This will be the first small exercise for the repo.
