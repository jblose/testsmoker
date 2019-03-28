# Set up using VirtualEnv
- $ cd smoker
- $ virtualenv venv
# Installing environment:
- $ pip install -r requirements.txt
# Preserve environment:
- $ pip freeze > requirements.txt
# Docker Build & Run
- $ docker build -t {tag name} .
- $ docker run -d -p 5000:5000 {tag name}
