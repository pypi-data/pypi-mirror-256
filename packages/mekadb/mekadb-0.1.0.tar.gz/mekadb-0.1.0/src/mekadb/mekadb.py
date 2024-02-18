import asyncio
import grpc
import json
import mekadb_client_pb2 as mekadb_client
import mekadb_client_pb2_grpc as mekadb_client_grpc


class MekaDBClient:
    def __init__(self, host='mekadb.hypi.app', port=443):
        self.host = host
        self.port = port
        self.channel = None
        self.stub = None
        self.request_id_counter = 0
        self.futures = {}

    async def connect(self):
        """Establishes a secure channel and initializes the stub."""
        self.channel = grpc.aio.secure_channel(
            f'{self.host}:{self.port}',
            grpc.ssl_channel_credentials()
        )
        self.stub = mekadb_client_grpc.MekaDBClientStub(self.channel)
        self.stream = self.stub.SqlWithJsonResponse()

    async def login(self, username, password, database, schema=None):
        """Authenticates and obtains an AuthCtx."""
        request = mekadb_client.AuthReq(username=username, password=password, database=database, schema=schema)
        response = await self.stub.authenticate(request)
        return response

    def _increment_request_id(self):
        self.request_id_counter += 1
        return self.request_id_counter

    def _convert_params_to_named_placeholders(self, params):
        """Converts params dict to NamedQueryPlaceHolder format."""
        placeholders = []
        for key, value in params.items():
            pv = mekadb_client.PlaceholderValue()
            if isinstance(value, int):
                pv.i64_t = value
            elif isinstance(value, float):
                pv.double_t = value
            elif isinstance(value, bool):
                pv.bool_t = value
            elif isinstance(value, str):
                pv.str_t = value
            else:
                raise ValueError("Unsupported parameter type")
            placeholders.append(mekadb_client.PlaceholderPair(name=key, value=pv))
        return mekadb_client.NamedQueryPlaceHolder(values=placeholders)

    async def query(self, creds, sql, params=None):
        """Sends a query request to the server."""
        request_id = self._increment_request_id()
        future = asyncio.get_event_loop().create_future()
        self.futures[request_id] = future

        sql_request = mekadb_client.SqlRequest(request_id=request_id, auth=creds, query=sql)
        if params:
            named_params = self._convert_params_to_named_placeholders(params)
            sql_request.named.CopyFrom(named_params)

        await self.stream.write(sql_request)

        return await future

    async def receive_responses(self):
        """Asynchronously receive responses from the server."""
        async for response in self.stream:
            if response.request_id in self.futures:
                future = self.futures.pop(response.request_id)
                if response.HasField('response'):
                    future.set_result(json.loads(response.response))
                elif response.HasField('error'):
                    future.set_exception(Exception(f"Error {response.error.code}: {response.error.message}"))

    async def close(self):
        """Closes the stream and channel."""
        await self.stream.done_writing()
        await self.channel.close()

    async def run(self):
        """Starts the client, establishing connection and preparing to receive responses."""
        await self.connect()
        asyncio.create_task(self.receive_responses())


if __name__ == '__main__':
    async def main():
        # Create an instance of the MekaDBClient
        client = MekaDBClient()
        # Connect to Hypi and keep a connection in the background
        await client.run()
        # Login to get authentication context
        auth = await client.login('<username>', '<password>', '<database name>')
        res = await client.query(creds=auth,
                                 sql='CREATE TABLE IF NOT EXISTS user(username VARCHAR, pass VARCHAR, PRIMARY KEY (username))')
        print("Create table:", res)
        res = await client.query(creds=auth,
                                 sql="INSERT INTO user(username,pass) VALUES('courtney','pass1'),('damion','pass2')")
        print("Insert:", res)
        res = await client.query(creds=auth, sql='SELECT * FROM user WHERE pass = :pass', params={'pass': 'pass99'})
        print("Select:", res)

        # Close the connection
        await client.close()


    # Run the main function within an asyncio event loop
    asyncio.run(main())
