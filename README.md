Code Documentation
General Description
This script implements a basic HTTP server using Python's http.server module to handle requests for creating, retrieving, updating, and deleting orders. It uses a simulated database (a list of dictionaries) to store orders and manages requests through the POST, GET, PUT, and DELETE methods. The application provides CRUD (Create, Read, Update, Delete) operations on orders, with support for filtering and pagination in GET requests.

Functionality
Create an Order (POST /orders)
Receives JSON data to create a new order, validates it, and saves it to a simulated database. If the order status is invalid, it responds with a 400 error.

Retrieve an Order by ID (GET /orders/{id})
Allows fetching the details of a specific order using its ID. If the order is not found, it responds with a 404 error.

List Orders (GET /orders)
Enables listing all orders with support for pagination and filtering by status. The page and page_size parameters control pagination, while the status parameter allows filtering orders by their status.

Update an Order (PUT /orders/{id})
Allows updating an existing order's details using its ID. The data can be partial; if a value is not provided, the current value is retained.

Delete an Order (DELETE /orders/{id})
Enables deleting an order by its ID. If the order is not found, it responds with a 404 error.

Technical Details
Simulated Database
The order database is an in-memory list of dictionaries (database = []). Each order has the following fields:

id: A unique identifier generated with uuid4().
customer_name: Name of the customer.
item: Name of the requested item.
quantity: Quantity of the requested item.
status: Order status (pending, completed, canceled).
created_at: Creation date in ISO 8601 format.
Allowed Order Statuses
The permitted statuses are "pending", "completed", and "canceled". Any other status in the request will be rejected with a 400 error.

Order Pagination and Filtering
The GET /orders request supports two optional parameters:

page: Page number (default is 1).
page_size: Number of orders per page (default is 10).
status: Allows filtering by order status (default is no status filter).
