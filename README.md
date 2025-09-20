# 🚀 Visitor Counter Flask App (with AWS DynamoDB + Jenkins CI/CD)

A simple **Flask web app** that increments a **visitor counter** stored in **AWS DynamoDB**.  
The app is containerized with **Docker**, images are pushed to **Amazon ECR**, and deployed to an **EC2 instance** through a **Jenkins pipeline**.

---

##  Features
- Flask app with a visitor counter.
- DynamoDB integration (atomic `UpdateItem` increments).
- Dockerized application.
- CI/CD with Jenkins:
  - Build & test app in Docker.
  - Push Docker image to Amazon ECR.
  - Deploy to EC2 via SSH.
- Works with both **AWS DynamoDB** and **DynamoDB Local** (for dev).

---

##  Project Structure

