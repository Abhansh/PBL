import json
import errno
import os
import threading
from subprocess import Popen, PIPE, STDOUT
from channels.generic.websocket import WebsocketConsumer

from PBL.settings import BASE_DIR


class OutputConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.proc = None
        self.thread = None

    def connect(self):
        self.accept()

    def disconnect(self, code):
        try:
            if self.proc:
                self.proc.terminate()
            if self.thread:
                self.thread.join()
        except Exception:
            pass

    def compile(self, path, file_type, filename, inputs):
        cmd = None
        if file_type == '.py':
            cmd = ['python', '-u', path + filename + file_type]

        elif file_type == '.java':
            self.proc = Popen(['javac', path + filename + file_type], stdout=PIPE, stderr=STDOUT)
            compile_op = self.proc.communicate()[0]
            self.proc.terminate()
            if compile_op:
                self.send(text_data=json.dumps({'output': compile_op.decode()}))
                return
            os.chdir(path)
            cmd = ['java', filename]

        elif file_type == '.cpp':
            self.proc = Popen(['g++', '-o', path+filename+'.exe', path+filename+file_type], stdout=PIPE, stderr=STDOUT)
            compile_op = self.proc.communicate()[0]
            self.proc.terminate()
            if compile_op:
                self.send(text_data=json.dumps({'output': compile_op.decode()}))
                return
            cmd = [path + filename]

        self.send_output(cmd, inputs)

    def send_output(self, process, inputs):
        self.proc = Popen(process, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        try:
            for inp in inputs:
                line = inp.encode('UTF-8')
                try:
                    self.proc.stdin.write(line)
                except IOError as e:
                    if e.errno == errno.EPIPE or e.errno == errno.EINVAL:
                        break
            self.proc.stdin.close()
            while True:
                line = self.proc.stdout.read(1)
                if line != b'\n':
                    self.send(text_data=json.dumps({'output': line.decode('UTF-8')}))
                if not line:
                    break
            self.send(text_data=json.dumps({'eof': True}))
        except TypeError as e:
            self.send(text_data=json.dumps({'output': str(e)}))
        finally:
            os.chdir(BASE_DIR)
            self.proc.terminate()

    def receive(self, text_data=None, bytes_data=None):
        request = json.loads(text_data)
        if 'stop' in request:
            if self.proc:
                self.proc.kill()
            if self.thread:
                self.thread.join()
        elif 'code' in request:
            path = 'Files/{}/'.format(request['user'])
            with open(path + request['filename'], 'w') as file:
                try:
                    file.write(request['code'])
                except IOError:
                    self.send(text_data=json.dumps({'output': 'Internal Server Error'}))
                    return
            inputs = input_splitter(request['inputs'])
            file_type = request['filename'][request['filename'].index('.'):]
            filename = request['filename'].replace(file_type, '')
            self.thread = threading.Thread(target=self.compile, args=(path, file_type, filename, inputs))
            self.thread.start()


def input_splitter(input_string):
    inputs = input_string.split('\n')
    final_inputs = []
    for x in inputs:
        final_inputs.append(x + '\n')
    return final_inputs
