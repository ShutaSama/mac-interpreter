from flask import Flask, request
import subprocess
import shlex

app = Flask(__name__)

@app.route('/execute-applescript', methods=['POST'])
def execute_applescript():
    try:
        script = request.json.get('script')
        if not script:
            return {'error': 'No script provided'}, 400
        process = subprocess.run(['osascript', '-e', script], text=True, capture_output=True)
        return {
            'stdout': process.stdout,
            'stderr': process.stderr,
            'returncode': process.returncode
        }
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/execute', methods=['POST'])
def execute_command():
    command = request.json['command']
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return {
        'stdout': result.stdout.decode('utf-8'),
        'stderr': result.stderr.decode('utf-8'),
        'returncode': result.returncode
    }

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5003)
