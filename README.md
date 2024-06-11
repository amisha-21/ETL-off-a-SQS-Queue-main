# ETL off a SQS Queue

Welcome to this project! The primary goal here is to craft an ETL pipeline that seamlessly fetches JSON data from an AWS SQS Queue, subtly masks the fields `device_id` and `ip` to ensure user privacy, and then diligently stores the transformed information into a PostgreSQL database.

## Requirements

- Python 3.11+
- PSQL
- Docker & Docker Compose
- pip or pip3
- awscli-local
- Python Libraries : psycopg2, and boto3.
   
## Getting Started

1. **Get the Code**: First things first, clone the repository:
   ```bash
   git clone https://github.com/dmohana1504/ETL-off-a-SQS-Queue
   ```
2. **Install Python Libraries**: If you do not have the Python libraries from the requirements then open PowerShell or Terminal, navigate to the repository folder, and run the command below:
   ```bash
   pip install -r modules.txt
   ```     
   
3. **Setting up**:
   - **For Windows users**: Simply right-click on `Run_Me_Windows` and choose 'Run with PowerShell'.
   - **For MacOS users**: Navigate to the repository folder in your terminal and execute:
     ```bash
     ./Run_Me_Mac.sh
     ```

4. **Database Details**: Whether you're on Windows or MacOS, our default PSQL credentials are:
   ```plaintext
   dbname: postgres
   user: postgres
   password: postgres
   host: localhost
   port: 5432
   ```

   If you're using different credentials, navigate to `Fetch-Rewards-Take-Home\Main` and adjust the values in the `connect_to_database` function within `DataOperations.py`.

5. **Connecting to the Database**:
   - **On Windows**: Open a PowerShell window and input:
     ```bash
     psql -d postgres -U postgres -p 5432 -h localhost -W
     ```

   - **On MacOS**: Fire up your SQL Shell (PSQL) and input:
     ```bash
     psql -d postgres -U postgres -p 5432 -h localhost -W
     ```

6. **Viewing the Data**: Once you're in the PSQL interface, simply use the following to view the table:
   ```sql
   SELECT * FROM user_logins;
   ```

## Troubleshooting & Tips

1. **Queue Messages**: If you stumble upon the "Queue is empty. No new messages to process." message, ensure that the localstack service is correctly set up with the pre-loaded messages. You can check the queue manually by running the command below using the Terminal or PowerShell:
   
   ```bash
   awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/login-queue
   ```

2. **Docker Hiccups**: Ensure that Docker services are up and running before executing the script. If you have any issues run the commands below to restart docker manually:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

3. **Running the Code**: Running into issues with the provided scripts? No worries! You can always run `Main.py` inside the `Fetch-Rewards-Take-Home\Main` directory using your favorite editor or terminal.

## Decision Points & Strategies

- **Reading from Queue**: Messages are fetched from the SQS Queue using `awslocal` commands.
- **Data Structures**: Lists and dictionaries in Python serve as our primary data structures, ensuring optimal performance and clarity.
- **Masking PII Data**: SHA-256 hashing aids in masking while retaining the capability to identify duplicate values.
- **Database Connection**: We use the psycopg2 Python library to establish a connection and write to Postgres.
- **Runtime Environment**: The entire application is containerized using Docker, making it platform-independent.

## Assumptions
- The Localstack image is pre-loaded with SQS messages.
- The Postgres image has all initial configurations set.
- The reader has a foundational understanding of Docker, PSQL, and AWS operations.

## Masking Mechanism

We prioritize user privacy by using SHA-256 hashing, which masks PII (Personal Identifiable Information) yet allows for data analysis by identifying duplicates.

## Deployment Strategy

Here's how we'd do it:
   
- **Containerize Everything**: We'd fit our application into containers using Docker. Then, employ Kubernetes to orchestrate these containers, ensuring smooth scalability and management.

- **Automate the Workflow**: Introducing CI/CD pipelines (think Jenkins or GitLab CI) can automate deployments. A new feature or fix? Let the pipeline handle testing and deployment once changes are pushed.

## Enhancements & Additions

What's on the horizon?

- **Improved Monitoring**: Integrating tools like Prometheus and Grafana can give us a hawk-eye view of our application's performance.
- **Better Error Management**: Imagine a system where potential faults trigger alerts, allowing for quick action. We're eyeing tools like PagerDuty or Opsgenie for this.
- **Tightened Security**: This involves encrypting data, managing secrets wisely, and setting up rigid access controls for our database.
- **Database Safeguards**: Regularly backing up our Postgres database to minimize any chances of data loss.

## Scalability Solutions

With data burgeoning, how does this application stand tall?

- **Horizontal Scaling**: By adding more instances of the application, we can share the load and serve more users.
- **Database Sharding**: Distributing database load across servers helps in managing vast amounts of data efficiently.
- **Smart Caching**: Implementing caching mechanisms like Redis to reduce frequent trips to the database.
- **Optimize Data Retrievals**: Ensuring our SQL queries are swift and efficient is a continual process.

## Recovering Original Data

Given the use of SHA-256 for masking, direct decryption isn't feasible. For data recovery, consider maintaining a secure mapping or storing the original encrypted data separately. Restricted individuals would have exclusive access.

## Contributions & Feedback

I am open to contributions and feedback to refine this solution further. Feel free to raise issues or suggest improvements.
