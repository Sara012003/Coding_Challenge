from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from uuid import uuid4, UUID
from datetime import datetime
from urllib.parse import parse_qs, urlparse

# Base de datos simulada
database = []

# Estados permitidos para los pedidos
ORDER_STATUSES = {"pending", "completed", "cancelled"}

# Clase para manejar solicitudes HTTP
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path == '/orders':
            # Leer y decodificar el cuerpo de la solicitud
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body)

            # Crear el nuevo pedido con validación básica
            order = {
                "id": str(uuid4()),
                "customer_name": data.get("customer_name"),
                "item": data.get("item"),
                "quantity": data.get("quantity"),
                "status": data.get("status"),
                "created_at": datetime.utcnow().isoformat()
            }

            # Validación del estado
            if order["status"] not in ORDER_STATUSES:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid status")
                return

            # Guardar el pedido en la "base de datos"
            database.append(order)
            self.send_response(201)
            self.end_headers()
            self.wfile.write(json.dumps(order).encode('utf-8'))

    def do_GET(self):
        # Obtener detalles de un pedido por ID
        if self.path.startswith('/orders/'):
            order_id = self.path.split('/')[-1]
            order = next((o for o in database if o["id"] == order_id), None)
            if order:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps(order).encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Order not found")

        # Listar todos los pedidos con paginación y filtro de estado
        elif self.path.startswith('/orders'):
            query = parse_qs(urlparse(self.path).query)
            page = int(query.get("page", [1])[0])
            page_size = int(query.get("page_size", [10])[0])
            status = query.get("status", [None])[0]

            # Filtrar y paginar
            orders = [o for o in database if not status or o["status"] == status]
            start = (page - 1) * page_size
            end = start + page_size
            paginated_orders = orders[start:end]

            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(paginated_orders).encode('utf-8'))

    def do_PUT(self):
        if self.path.startswith('/orders/'):
            order_id = self.path.split('/')[-1]
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body)

            # Buscar y actualizar el pedido
            order = next((o for o in database if o["id"] == order_id), None)
            if order:
                order.update({
                    "customer_name": data.get("customer_name", order["customer_name"]),
                    "item": data.get("item", order["item"]),
                    "quantity": data.get("quantity", order["quantity"]),
                    "status": data.get("status", order["status"])
                })
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps(order).encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Order not found")

    def do_DELETE(self):
        if self.path.startswith('/orders/'):
            order_id = self.path.split('/')[-1]
            global database
            initial_length = len(database)
            database = [o for o in database if o["id"] != order_id]

            if len(database) < initial_length:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Order deleted")
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Order not found")

# Configuración del servidor
def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print('Server running on port 8000...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
