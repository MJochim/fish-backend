debug_mode = True
cgi_trace_logdir = "/var/log/fish/cgilogs"

data_directory = "/var/lib/fish/questionnaires_collection"

password = ""

base_url = "/fish"

token_url = "https://keycloak.example.com/auth/realms/master/protocol/openid-connect/token"
introspection_url = "https://keycloak.example.com/auth/realms/master/protocol/openid-connect/token/introspect"
keycloak_realm_api_url = "https://keycloak.example.com/auth/admin/realms/master"
client_id = "fish-backend"
client_secret = ""
frontend_client_uuid = ""

headers = {
	"Access-Control-Allow-Origin": "*",
	"Access-Control-Allow-Headers": "authorization,content-type",
	"Access-Control-Allow-Methods": "GET,PATCH,PUT,DELETE"
}

smtp_host = "smtp.example.com"
smtp_local_hostname = "api.example.com"
smtp_username = ""
smtp_password = ""
