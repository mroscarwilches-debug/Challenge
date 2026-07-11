# A small image with Python already installed - no need for a bigger one.
FROM python:3.12-slim

WORKDIR /app

# Copy just this file first. That way, if only our code changes later
# (not the dependencies), Docker can reuse the already-installed
# packages instead of redoing this step.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now bring in the rest of the code.
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
