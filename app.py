from pushups_logger import create_app
from flask import request
from flask import jsonify
app = create_app()

@app.route('/hello', methods=['GET'])
def helloworld():
    if(request.method == 'GET'):
        data = {"data": "Hello World"}
        return jsonify(data)

if __name__ == "__main__":
    app.run()
