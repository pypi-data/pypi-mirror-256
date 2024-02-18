import datetime
import requests
from panda_pos_api.graphql_query_builder import get_query_arguments
from graphql_query import Operation, Query, Field as GraphQLField
from panda_pos_api.models import Ticket, Product, ProductTag



class GraphQL:
    
    
    def __init__(self, username: str, password: str, client_id: str, client_secret: str, message_server_host: str, message_server_port: str) -> None:
        self.session = requests.Session()
        self.username = username
        self.password = password
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_expired_timestamp: int = None
        self.message_server_url = f"{message_server_host}:{message_server_port}"
        self.access_token = None
        self.headers = {
            "Authorization": ""
        }
    
    
    def request(self, url: str, method: str, data: dict = {}, params: dict = {}, json: dict = {}, timeout: int = 5):
        if self.access_token is None or  self.token_expired_timestamp < datetime.datetime.timestamp(datetime.datetime.now()):
            token_json = self.get_token()
            self.access_token = token_json["access_token"]
            self.token_expired_timestamp = datetime.datetime.timestamp(datetime.datetime.now()) + token_json["expires_in"]
        
        self.headers.update({"Authorization": f"Bearer {self.access_token}"})
        
        res = self.session.request(method=method, url=url, data=data, json=json, params=params, timeout=timeout, headers=self.headers)
        if res.json()["errors"]:
            for error in res.json()["errors"]:
                print(f"""
                      Message: {error['innerException']['Message']}
                      Param: {error['innerException']['ParamName']}
                      """)
                print(error["message"])
            return None
        
        return res.json()
    
    def get_token(self):
        data = {
            "grant_type": "password",
            "username": "esat",
            "password": "esat3535",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        
        res = self.session.post(f"{self.message_server_url}/Token", data=data)
        return res.json()
    
    
    def get_graphql_query_str(self, operation_type: str, operation_name: str, payload: dict, fields: list[str] = []):
        graphql_operation = Operation(
            name="m",
            type=operation_type,
            queries=[
                Query(
                    name=operation_name,
                    arguments=get_query_arguments(payload),
                    fields=fields,
                    
                    
                )
            ]
        )
        return graphql_operation.render()
    
    
    def register_terminal(self, user: str, ticketType: str, terminal: str, department: str) -> str:
        mutation_name = "registerTerminal"
        params = {
            "user": user,
            "ticketType": ticketType,
            "terminal": terminal,
            "department": department
        }
                
        payload = {
            "operationName": "m",
            "query": self.get_graphql_query_str("mutation", mutation_name, params),
        }
        res = self.request(f"{self.message_server_url}/api/graphql", method="POST", json=payload)
        return res["data"]["registerTerminal"]

    
    
    def unregister_terminal(self, id: str):
        params = {
            "terminalId": id,
        }
        
        payload = {
            "operationName": "m",
            "query": self.get_graphql_query_str("mutation", "unregisterTerminal", params),
        }
        
        self.request(f"{self.message_server_url}/api/graphql/", method="POST", json=payload)
        return "Ok."
    
    
    
    def create_ticket(self, ticket: Ticket):
        mutation_name = "addTicket"
        payload = {
            "operationName": "m",
            "query": self.get_graphql_query_str("mutation", mutation_name, {"ticket": ticket.dict()}, fields=[]),
        }
        res = self.request(f"{self.message_server_url}/api/graphql", method="POST", json=payload)
        return res
    
    def create_terminal_ticket(self, terminal_id: str) -> str:
        mutation_name = "createTerminalTicket"
        params = {
            "terminalId": terminal_id 
        }
                
        payload = {
            "operationName": "m",
            "query": self.get_graphql_query_str("mutation", mutation_name, params, fields=["uid"]),
            
        }
        res = self.request(f"{self.message_server_url}/api/graphql", method="POST", json=payload)
        return res["data"]["createTerminalTicket"]["uid"]
    
    
    
    def add_product(self, product: Product):
        mutation_name = "addProduct"
        
        payload = {
            "operationName": "m",
            "query": self.get_graphql_query_str("mutation", mutation_name, product.dict(), fields=["id"]),
            
        }
        res = self.request(f"{self.message_server_url}/api/graphql", method="POST", json=payload)
        return res["data"]["addProduct"]["id"]
    
    
    def get_product(self, name: str = "", id: str = ""):
        query_name = "getProduct"
        payload = {
            "operationName": "m",
            "query": self.get_graphql_query_str("query", query_name, {"name": name, "id": id}, fields=["id", "name", "groupCode", "barcode", GraphQLField(name="portions", fields=["id", "name", "price"]), "tags"])
        }
        res = self.request(f"{self.message_server_url}/api/graphql", method="POST", json=payload)
        return res["data"]["getProduct"]
    
    def get_all_products(self):
        query_name = "getProducts"
        payload = {
            "operationName": "m",
            "query": self.get_graphql_query_str("query", query_name, {}, fields=["id", "name", "groupCode", "barcode", GraphQLField(name="portions", fields=["id", "name", "price"]), "tags"])
        }
        res = self.request(f"{self.message_server_url}/api/graphql", method="POST", json=payload)
        return res["data"]["getProducts"]
    
    def get_products_by_tag(self, productTag: ProductTag):
        query_name = "getProducts"
        payload = {
            "operationName": "m",
            "query": self.get_graphql_query_str("query", query_name, {"itemTag": productTag.dict()}, fields=["id", "name", "groupCode", "barcode", GraphQLField(name="portions", fields=["id", "name", "price"]), "tags"])
        }
        res = self.request(f"{self.message_server_url}/api/graphql", method="POST", json=payload)
        return res["data"]["getProducts"]
    
    def get_products_by_barcode(self, barcode: str):
        query_name = "getProducts"
        payload = {
            "operationName": "m",
            "query": self.get_graphql_query_str("query", query_name, {"barcode": barcode}, fields=["id", "name", "groupCode", "barcode", GraphQLField(name="portions", fields=["id", "name", "price"]), "tags"]),
        }
        res = self.request(f"{self.message_server_url}/api/graphql", method="POST", json=payload)
        return res["data"]["getProducts"]
    
    def get_products_by_groupCode(self, groupCode: str):
        query_name = "getProducts"
        payload = {
            "operationName": "m",
            "query": self.get_graphql_query_str("query", query_name, {"groupCode": groupCode}, fields=["id", "name", "groupCode", "barcode", GraphQLField(name="portions", fields=["id", "name", "price"]), "tags"]),
        }
        res = self.request(f"{self.message_server_url}/api/graphql", method="POST", json=payload)
        return res["data"]["getProducts"]
    
