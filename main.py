# -*- coding: utf-8 -*-
# ClassIslandManagementServer/main.py
import asyncio
import logging
import uuid

import grpc

import launcher as launcher

# 配置日志记录器
from Protobuf.Client import ClientRegisterCsReq_pb2, ClientCommandDeliverScReq_pb2
from Protobuf.Enum import Retcode_pb2, CommandTypes_pb2
from Protobuf.Server import ClientCommandDeliverScRsp_pb2
from Protobuf.Service import ClientRegister_pb2_grpc, ClientCommandDeliver_pb2_grpc
from Protobuf.Command import SendNotification_pb2

async def register_client(channel, client_uid, client_id="TestClient"):
    """Helper function to register a client."""
    stub = ClientRegister_pb2_grpc.ClientRegisterStub(channel)
    request = ClientRegisterCsReq_pb2.ClientRegisterCsReq(
        clientUid=client_uid,
        clientId=client_id
    )
    response = await stub.Register(request)
    return response

async def listen_for_commands(channel, client_uid, expected_commands, timeout=65):
    """
    Helper function to listen for commands from the server.

    Args:
        channel: The gRPC channel.
        client_uid: The client UID.
        expected_commands: A list of (command_type, payload_checker) tuples.
            payload_checker is a function that takes the payload bytes and returns True if valid.
        timeout: Timeout in seconds.

    Returns:
        True if all expected commands were received, False otherwise.
    """
    stub = ClientCommandDeliver_pb2_grpc.ClientCommandDeliverStub(channel)
    metadata = [('cuid', client_uid)]
    received_commands = []

    async def request_stream():
        # Send a Ping initially to establish the stream
        yield ClientCommandDeliverScReq_pb2.ClientCommandDeliverScReq(Type=CommandTypes_pb2.Ping)
        # Keep the connection alive by sending pings.  Important for long-running tests.
        while True:
            await asyncio.sleep(10)  # Send Ping every 10 seconds
            yield ClientCommandDeliverScReq_pb2.ClientCommandDeliverScReq(Type=CommandTypes_pb2.Ping)

    try:
        async for response in stub.ListenCommand(request_stream(), metadata=metadata, timeout=timeout):
            if response.RetCode != Retcode_pb2.Success:
                print(f"Server returned error: {response.RetCode}")
                return False

            for expected_type, payload_checker in expected_commands:
                if response.Type == expected_type:
                    if payload_checker is None or payload_checker(response.Payload):
                        received_commands.append((response.Type, response.Payload))
                        break  # Move to the next expected command

            if len(received_commands) == len(expected_commands):
                return True  # Got all expected commands

        # If we exit the loop without returning True, we didn't get all commands
        print(f"Did not receive all expected commands.  Received: {received_commands}")
        return False
    except grpc.aio.AioRpcError as e:
        print(f"gRPC error: {e}")
        return False
    except asyncio.TimeoutError:
        print(f"Timeout while listening for commands")
        return False



async def test_basic_notification():
    """Test sending a basic notification."""
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        client_uid = str(uuid.uuid4())
        await register_client(channel, client_uid)

        def check_payload(payload_bytes):
            notification = SendNotification_pb2.SendNotification.FromString(payload_bytes)
            return (notification.MessageMask == "Test Mask" and
                    notification.MessageContent == "Test Content")

        received = await listen_for_commands(channel, client_uid, [
            (CommandTypes_pb2.SendNotification, check_payload)
        ])
        assert received, "Basic notification not received"
        print("Test Basic Notification: PASSED")


async def test_emergency_notification():
    """Test the IsEmergency flag."""
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        client_uid = str(uuid.uuid4())
        await register_client(channel, client_uid)

        def check_payload(payload_bytes):
            notification = SendNotification_pb2.SendNotification.FromString(payload_bytes)
            return notification.IsEmergency

        received = await listen_for_commands(channel, client_uid, [
            (CommandTypes_pb2.SendNotification, check_payload)
        ])
        assert received, "Emergency notification not received"
        print("Test Emergency Notification: PASSED")


async def test_notification_settings():
    """Test notification settings (speech, effect, sound, topmost)."""
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        client_uid = str(uuid.uuid4())
        await register_client(channel, client_uid)

        def check_payload(payload_bytes):
            notification = SendNotification_pb2.SendNotification.FromString(payload_bytes)
            return (notification.IsSpeechEnabled and
                    not notification.IsEffectEnabled and
                    notification.IsSoundEnabled and
                    not notification.IsTopmost)

        received = await listen_for_commands(channel, client_uid, [
            (CommandTypes_pb2.SendNotification, check_payload)
        ])
        assert received, "Notification settings not received correctly"
        print("Test Notification Settings: PASSED")


async def test_duration_and_repetition():
    """Test duration and repetition settings."""
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        client_uid = str(uuid.uuid4())
        await register_client(channel, client_uid)

        def check_payload(payload_bytes):
            notification = SendNotification_pb2.SendNotification.FromString(payload_bytes)
            return notification.DurationSeconds == 5 and notification.RepeatCounts == 3

        received = await listen_for_commands(channel, client_uid, [
            (CommandTypes_pb2.SendNotification, check_payload)
        ])
        assert received, "Duration/repetition not received correctly"
        print("Test Duration and Repetition: PASSED")

async def test_invalid_command():
    """Test handling of invalid command types."""
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        client_uid = str(uuid.uuid4())
        await register_client(channel, client_uid)
        received = await listen_for_commands(channel, client_uid, [
            (CommandTypes_pb2.RestartApp, None)  # We expect *not* to receive this
        ], timeout=10) # short timeout
        assert not received, "Invalid Command Processed"
        print("Test Invalid Command: PASSED")



async def run_all_tests():
    """Runs all test cases."""
    await test_basic_notification()
    await test_emergency_notification()
    await test_notification_settings()
    await test_duration_and_repetition()
    await test_invalid_command()
    # await test_client_disconnect()  # Add this back when implemented
    # await test_multiple_clients() # Add this back when implemented


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(register_client())
    # Start the server in a separate thread
    # import threading
    # threading.Thread(target=launcher.run_server, daemon=True).start()
    # asyncio.run(run_all_tests())