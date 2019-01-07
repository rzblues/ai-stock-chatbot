from rasa_nlu.model import Interpreter
import json

interpreter = Interpreter.load("./models/current/nlu")
message = "let's see some apple price"
result = interpreter.parse(message)
print(json.dumps(result, indent=2))