# Billogram Task  
  
There are two endpoints. One to create discount codes and another to get discount codes.  

### Prerequisites
Install docker. To install docker follow the following documentation
https://docs.docker.com/engine/install/

### To run the solution use the following command

    docker compose up

  
### Create new discount codes  
  
To create new discount coder run the following curl command.

    curl --location --request POST 'http://127.0.0.1:5000/api/v1/discount/code' \
	--header 'Content-Type: application/json' \
	--data-raw '{
	"brand_id": 1,
	"total_codes": 5,
	"discount_percentage": 5,
	"expiry_date": 1656502310
	}'

### Get new discount code

    curl --location --request GET 'http://127.0.0.1:5000/api/v1/discount/code?brand_id=1'
