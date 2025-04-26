File Upload System with Token Authentication

This project implements a secure file upload system using Flask, AWS S3, and PostgreSQL (RDS). It verifies tokens issued by AWS Cognito before allowing file uploads.

Features

1.Secure authentication using JWT tokens validated against AWS Cognito.

2.Uploads files to Amazon S3 bucket under the uploads/ prefix.

3.Saves file metadata (upload_id, filename, S3 key, upload timestamp) into PostgreSQL RDS.

4.Supports only PDF, DOCX, and TXT files.

5.Automatic timestamp added to filenames to avoid overwriting.

6.Tokens expire after 5 minutes for enhanced security.



1. Token Generation (/auth/token):
    1.1	Client (like Postman) sends a POST request to /auth/token with:
           clientId
           secret
           scope
    1.2 The custom Auth API (/auth/token) acts as a middleware layer, and internally:
            Calls Cognito’s token endpoint (e.g., /oauth2/token)
            Passes the client credentials and scope to Cognito
    
    1.3 Cognito:
        	Validates the credentials
        	If valid → generates the token and returns it to the Auth API
        	If invalid: Cognito returns an error, which is forwarded back by the Auth API.

    1.4 Auth API:
            Returns Cognito's token back to the client
2.Document Upload (/upload):
	   -The request will include:
	       -Bearer token in the Authorization header.
        	-Document file (in body).
    	-Inside the /upload API:
            -First, it will call /auth/validate to verify the token.
        	-If the token is valid:
            	-Perform validation on the uploaded document:
                	-Check if the file is not empty.
                	=Check if the file is in allowed formats (PDF, DOC, or TXT).
            	-If file validation passes:
                    Upload the document to an S3 bucket.
                    Store metadata about the upload in the RDS (Relational Database Service).
                -If the token is invalid:
                	Return an error response without proceeding further.


    


