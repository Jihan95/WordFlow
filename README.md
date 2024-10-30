## WordFlow API

# Project Overview

WordFlow is a RESTful API designed for a blog platform that allows users to create, read, update, and delete blog posts, manage user accounts, and enable authentication for a secure and personalized experience. Built using Python, Flask, and MySQL, WordFlow is intended to support scalable, high-performance blog applications.

Table of Contents
Getting Started
API Endpoints
Authentication
Architecture and Technology
Development Progress
Future Enhancements
Team
License
Getting Started
Prerequisites
Python 3.8+
MySQL (or another SQL database supported by SQLAlchemy)
Flask and other dependencies listed in requirements.txt
Installation

# Clone the Repository:

git clone https://github.com/Jihan95/WordFlow.git
cd WordFlow

# Install Dependencies:

pip install -r requirements.txt

# Configure the Database:

Create a MySQL database.
Update the db_config parameters in config.py with your database details.

# Start the Server:

flask run
The API server will be available at http://localhost:5000.

## API Endpoints

Below is a list of core endpoints in the WordFlow API. Detailed documentation for each endpoint can be found in docs/api_documentation.md.

# Users

POST /api/v1/users/register - Register a new user.
POST /api/v1/users/login - Login and receive a JWT token.
GET /api/v1/users/profile - Retrieve authenticated user's profile.

# Blogs

GET /api/v1/blogs - List all blogs.
POST /api/v1/blogs - Create a new blog post.
GET /api/v1/blogs/<id> - Retrieve a specific blog post.
PUT /api/v1/blogs/<id> - Update a blog post.
DELETE /api/v1/blogs/<id> - Delete a blog post.

# Comments

POST /api/v1/blogs/<id>/comments - Add a comment to a blog post.
GET /api/v1/blogs/<id>/comments - Retrieve comments for a specific blog post.
Authentication
WordFlow API uses JWT-based authentication. After logging in, users receive a token that they must include in the Authorization header as Bearer <token> with each request to protected endpoints.

# Architecture and Technology

WordFlow is developed with a focus on scalability, security, and ease of extension. Key technologies include:

Flask - Provides the lightweight framework for API development.
MySQL - Used for relational data storage.
SQLAlchemy - Handles ORM functionality.
JWT - Manages secure, token-based authentication.
Development Progress
The WordFlow API project is currently in the development stage. Key progress includes:

Completed: Basic CRUD for blogs, user registration, authentication.
In Progress: User profile management, comment features.
Challenges: Implementing optimized query handling and pagination.
Next Steps: Implement advanced filtering and tagging for posts, and finalize API documentation.
Future Enhancements
In future iterations, we plan to:

Improve user interaction with advanced tagging, search, and filtering.
Enhance the API security with role-based permissions.
Build frontend integrations for improved UX.
Team
Jihan Ahmed Mahmoud

# License

This project is licensed under the MIT License - see the LICENSE file for details.

Happy Blogging with WordFlow!
