# Backend Project

This is the backend code for website which template i found in internet. It includes various features and enhancements added by me, including integration of Celery, RabbitMQ, and Redis for improved performance and task processing.

Features:
1. Celery: Task processing and asynchronous operations.
2. RabbitMQ: Message queuing for efficient task distribution.
3. Redis: Caching for improved performance.
4. Fully tested: Comprehensive unit tests have been written and executed to ensure functionality and reliability.

## Prerequisites

Before running the backend, ensure you have the following components installed:

- Python 3.x
- Django
- Celery
- RabbitMQ
- Redis

## Getting Started

Follow these steps to set up and run the backend:

1. Clone the repository:
git clone https://github.com/SaskerSours/Backend-project.git
2. Install the required dependencies:
pip install -r requirements.txt
3. Set up Django configurations and database settings:
4. Start the Celery worker and Reddis + RabbitMQ:
celery -A your_django_project_name worker -l info
5. Run the Django development server:

## Contribution

Feel free to contribute to this project by submitting pull requests or reporting issues. If you see any problems, please write



