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

import time
import grpc

import array_pb2_grpc
import array_pb2

SERVER_ADDRESS = "localhost:23333"
CLIENT_ID = 1

def array_method(stub):
    print("--------------Call SignalMethod Begin--------------")
    request = array_pb2.ArrayRequest(
        client_id=CLIENT_ID, data=[1,2,3])
    response = stub.ArrayMethod(request)
    print("resp from server(%d), the message=%s" % (response.server_id,
                                                    response.data))
    print("--------------Call SignalMethod Over---------------")

def bidirectional_streaming_method(stub):
    print("--------------Call BidirectionalStreamingMethod Begin---------------")

    def request_messages():
        for i in range(5):
            request = array_pb2.ArrayRequest(
                client_id=CLIENT_ID, data=[1,2,3])
            yield request
            time.sleep(2)

    response_iterator = stub.BidirectionalArrayMethod(request_messages())
    for response in response_iterator:
        print("recv from server(%d), message=%s" % (response.server_id,
                                                    response.data))

    print("--------------Call BidirectionalStreamingMethod Over---------------")


def main():
    with grpc.insecure_channel(SERVER_ADDRESS) as channel:
        stub = array_pb2_grpc.ArrayDemoStub(channel)

        array_method(stub)
        bidirectional_streaming_method(stub)
        
if __name__ == '__main__':
    main()
