import json
from channels.generic.websocket import AsyncWebsocketConsumer
from pages.models import Page
from .ot.operations import Insert, Delete
# import asyncio
import websockets


class PageEditConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.page_id = self.scope["url_route"]["kwargs"]["page_id"]
        self.page_group_name = f"page_{self.page_id}"

        await self.channel_layer.group_add(self.page_group_name, self.channel_name)
        await self.accept()

        # Send current page content to the newly connected client
        page = await Page.objects.aget(pk=self.page_id)
        await self.send(
            text_data=json.dumps(
                {
                    "type": "page_content",
                    "content": page.content,
                }
            )
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.page_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        op_type = text_data_json["type"]

        if op_type == "insert":
            operation = Insert(text_data_json["text"], text_data_json["pos"])
        elif op_type == "delete":
            operation = Delete(text_data_json["length"], text_data_json["pos"])
        else:
            return

        page = await Page.objects.aget(pk=self.page_id)
        new_content = operation.apply(page.content)
        page.content = new_content
        await page.asave()

        # Broadcast the operation to other clients in the group
        await self.channel_layer.group_send(
            self.page_group_name,
            {
                "type": "page_edit",
                "operation_type": op_type,
                "text": text_data_json.get("text"),
                "pos": text_data_json.get("pos"),
                "length": text_data_json.get("length"),
                "sender_channel": self.channel_name,  # Exclude sender from receiving the update
            },
        )

    async def page_edit(self, event):
        # Send the received operation to other clients (excluding the sender)
        if self.channel_name != event["sender_channel"]:
            await self.send(
                text_data=json.dumps(
                    {
                        "type": event["operation_type"],
                        "text": event.get("text"),
                        "pos": event.get("pos"),
                        "length": event.get("length"),
                    }
                )
            )

    # Client-side code to consume the WebSocket
    async def consume():
        uri = "ws://localhost:8000/ws/page/<page_id>/"
        async with websockets.connect(uri) as websocket:
            # Receive initial page content
            initial_content = await websocket.recv()
            print(f"Initial content: {initial_content}")

            # Send an insert operation
            insert_operation = json.dumps(
                {"type": "insert", "text": "Hello, World!", "pos": 0}
            )
            await websocket.send(insert_operation)

            # Receive the broadcasted operation
            response = await websocket.recv()
            print(f"Received: {response}")

            # Send a delete operation
            delete_operation = json.dumps({"type": "delete", "length": 5, "pos": 0})
            await websocket.send(delete_operation)

            # Receive the broadcasted operation
            response = await websocket.recv()
            print(f"Received: {response}")

    # # Run the consume function
    # asyncio.get_event_loop().run_until_complete(consume())
