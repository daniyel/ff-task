from waitress import serve
from main import app as myapp

serve(myapp, host="0.0.0.0", port="5000")
