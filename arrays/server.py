# Copyright 2019 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The example of four ways of data transmission using gRPC in Python."""

from threading import Thread
from concurrent import futures
import time

import grpc
import array_pb2_grpc
import array_pb2

SERVER_ADDRESS = 'localhost:23333'
SERVER_ID = 1


class ArrayServer(array_pb2_grpc.ArrayDemoServicer):
    def ArrayMethod(self, request, context):
        print("SimpleMethod called by client(%d) the message: %s" %
              (request.client_id, request.data))

        response = array_pb2.ArrayResponse(
        server_id=SERVER_ID, data=[4,5,6])
        return response

    def BidirectionalArrayMethod(self, request_iterator, context):
            print("BidirectionalStreamingMethod called by client...")

            # 开启一个子线程去接收数据
            # Open a sub thread to receive data
            def parse_request():
                for request in request_iterator:
                    print("recv from client(%d), message= %s" %
                        (request.client_id, request.data))

            t = Thread(target=parse_request)
            t.start()

            for i in range(5):
                response = array_pb2.ArrayResponse(
                    server_id=SERVER_ID, data=[4,5,6])
                yield response
                time.sleep(1)

            t.join()

def main():
    server = grpc.server(futures.ThreadPoolExecutor())

    array_pb2_grpc.add_ArrayDemoServicer_to_server(ArrayServer(), server)

    server.add_insecure_port(SERVER_ADDRESS)
    print("------------------start Python GRPC server")
    server.start()
    server.wait_for_termination()

    # If raise Error:
    #   AttributeError: '_Server' object has no attribute 'wait_for_termination'
    # You can use the following code instead:
    # import time
    # while 1:
    #     time.sleep(10)


if __name__ == '__main__':
    main()
