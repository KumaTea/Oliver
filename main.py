import taskManager
from starting import starting
from flask import Flask, request as flask_req
try:
    from localTools import get_token
except ImportError:
    def get_token(cmd): return cmd


app = Flask(__name__)


@app.route('/trigger', methods=['POST'])
def trigger():
    data = flask_req.form
    if 'command' in data and 'token' in data:
        command = data['command']
        token = data['token']
        correct_token = get_token(command)
        if token == correct_token:
            if command in taskManager.available_tasks:
                result = getattr(taskManager, command)()
                return f'Done.\nResult: {result}', 200
            else:
                return 'No such command.', 404
        else:
            return 'Token Error.', 403
    else:
        return 'Missing command or token.', 400


@app.route('/', methods=['GET'])
def status():
    return 'Oliver bot is running.', 200


# If run on local machine:
if __name__ == '__main__':
    starting()
    taskManager.manager()
    taskManager.scheduler.start()
    app.run(host='localhost', port=10570, debug=False)
