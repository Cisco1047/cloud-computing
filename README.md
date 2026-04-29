# Cloud Computing Project - Quote Generator  

This project is a modern, serverless web application that retrieves random fortunes from a database. It is designed to be highly scalable, secure, and cost-efficient by leveraging AWS managed services.

## Technical Stack

| Service | Role |
| :--- | :--- |
| **Amazon S3** | Static Web Hosting |
| **AWS Lambda** | Serverless Compute (Python 3.9) |
| **Amazon DynamoDB** | NoSQL Database |
| **Amazon API Gateway** | RESTful API Integration |

---

## 1. Prerequisites & Environment Setup

Before starting the deployment, ensure the following tools are installed and configured:

* **Git Bash:** Required for executing shell scripts and managing the project directory on Windows.
* **AWS CLI:** Must be installed and configured with your credentials using `aws configure`.
* **Python 3.9:** The required runtime for the backend Lambda function.
* **Project Files:** Ensure your project folder contains `lambda_function.py` and the `frontend/` directory.

---

## 2. Database Layer: Amazon DynamoDB

The application uses a NoSQL database to store the collection of fortunes.

1.  **Create Table:** Create a table named `Fortunes` in your preferred region (e.g., `us-east-1`).
2.  **Define Schema:** Use `id` as the **Partition Key** (String).
3.  **Add Data:** Ensure items in the table have an attribute named `text` (lowercase) containing the fortune string.

---

## 3. Backend Layer: AWS Lambda

Deploy the serverless Python logic to handle data retrieval.

1.  **Prepare the Package:** Open Git Bash in your project folder and zip the script:
    ```bash
    zip lambda_function.zip lambda_function.py
    ```
2.  **IAM Role Setup:** * Create a role in the IAM Console with a **Trust Policy** allowing `lambda.amazonaws.com` to assume the role.
    * Attach permissions for **AmazonDynamoDBReadOnlyAccess** and **AWSLambdaBasicExecutionRole** (for CloudWatch logging).
3.  **Deploy via CLI:**
    ```bash
    aws lambda create-function --function-name getFortune \
    --runtime python3.9 --handler lambda_function.lambda_handler \
    --zip-file fileb://lambda_function.zip \
    --role YOUR_LAMBDA_ROLE_ARN \
    --environment Variables="{FORTUNE_TABLE=Fortunes}" --region us-east-1
    ```
    *(Note: The `fileb://` prefix is required for binary uploads in Git Bash).*

---

## 4. API Layer: Amazon API Gateway

The API Gateway acts as the bridge between your frontend and the Lambda function.

1.  **Create HTTP API:** Select **Build** under HTTP API in the AWS Console.
2.  **Configure Integration:** Add your `getFortune` Lambda function as the integration.
3.  **Set Route:** Create a `GET` route with the path `/api/fortune`.
4.  **Enable CORS:** In the CORS settings menu:
    * **Access-Control-Allow-Origin:** `*`
    * **Access-Control-Allow-Methods:** `GET`
    * **Access-Control-Allow-Headers:** `Content-Type`
5.  **Note Invoke URL:** Copy the **Invoke URL** from the Stages tab (e.g., `https://xyz.execute-api.us-east-1.amazonaws.com`).

---

## 5. Frontend Layer: Amazon S3

Host the user interface as a static website.

1.  **Update Fetch URL:** In your local frontend JavaScript code, update the `fetch()` call to point to your new API Gateway URL:
    ```javascript
    const response = await fetch('https://[your-api-id].execute-api.us-east-1.amazonaws.com/api/fortune');
    ```
2.  **Create Bucket:** Create a bucket in S3 (e.g., `my-fortune-cookie-site`). Disable "Block all public access."
3.  **Upload Files:** Upload the *contents* of your `frontend` folder directly to the root of the bucket (ensure `index.html` is at the top level).
4.  **Enable Hosting:**
    * Go to **Properties** > **Static website hosting**.
    * Select **Enable** and set the **Index document** to `index.html`.
5.  **Set Bucket Policy:** Add a policy to the **Permissions** tab to allow public read access:
    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME/*"
            }
        ]
    }
    ```

---

## 6. Verification

1.  Navigate to the **Bucket website endpoint** provided in the S3 Properties tab.
2.  Open the browser console (F12) to check for any errors.
3.  Interact with the page to verify the Lambda function successfully fetches a random fortune from DynamoDB.
