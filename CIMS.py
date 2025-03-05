# CIMS.py
import ManagementServer
import asyncio
import json
import argparse
import sys


def load_settings(settings_file="settings.json"):
    """Loads settings from a JSON file or creates a default one."""
    try:
        with open(settings_file) as s:
            settings = json.load(s)
    except FileNotFoundError:
        settings = {
            "ports": {
                "gRPC": 50051,
                "command": 50052,
                "api": 50050,
                "webui": 50053,
            },
            "organization_name": "CMS2.py 本地测试",
            "host": "0.0.0.0"
        }
        with open(settings_file, "w") as s:
            json.dump(settings, s, indent=4)
    return settings


async def start_servers(settings):
    """Starts the gRPC, command, and API servers."""
    await asyncio.gather(
        ManagementServer.gRPC.start(settings["ports"]["gRPC"]),
        ManagementServer.command.start(settings["ports"]["command"]),
        ManagementServer.api.start(settings["ports"]["api"], settings["host"])
    )


async def main():
    """Main function to parse arguments and start servers."""
    parser = argparse.ArgumentParser(description="ClassIsland Management Server (CIMS)")
    parser.add_argument("-c", "--config", type=str, default="settings.json", help="Path to the settings JSON file.")
    parser.add_argument("-g", "--grpc", type=int, help="Override gRPC port from settings.")
    parser.add_argument("-m", "--command", type=int, help="Override command port from settings.")
    parser.add_argument("-a", "--api", type=int, help="Override API port from settings.")
    parser.add_argument("-w", "--webui", type=int, help="Override WebUI port from settings.")
    parser.add_argument("-H", "--host", type=str, help="Override host address from settings.")
    parser.add_argument("-l", "--list-ports", action="store_true",
                        help="List the current configuration ports then exit.")
    parser.add_argument("-p", "--generate-management-preset", action="store_true",
                        help="Generate ManagementPreset.json")

    args = parser.parse_args()

    settings = load_settings(args.config)

    if args.list_ports:
        print("Current Configuration Ports:")
        print(f"  gRPC:    {settings['ports']['gRPC']}")
        print(f"  Command: {settings['ports']['command']}")
        print(f"  API:     {settings['ports']['api']}")
        print(f"  WebUI:   {settings['ports']['webui']}")
        print(f"  Host:    {settings['host']}")
        sys.exit(0)

    if args.generate_management_preset:
        with open("ManagementPreset.json", "w") as mp:
            json.dump({
                "ManagementServerKind": 1,
                "ManagementServer": f"http://{settings["host"]}:{settings["ports"]["api"]}",
                "ManagementServerGrpc": f"http://{settings["host"]}:{settings["ports"]["gRPC"]}",
            }, mp)
        sys.exit(0)

    # Override ports if provided as arguments
    if args.grpc:
        settings["ports"]["gRPC"] = args.grpc
    if args.command:
        settings["ports"]["command"] = args.command
    if args.api:
        settings["ports"]["api"] = args.api
    if args.webui:
        settings["ports"]["webui"] = args.webui
    if args.host:
        settings["host"] = args.host

    print("Starting ClassIsland Management Server (CIMS) with these configurations:")
    print(f"  gRPC:    {settings['ports']['gRPC']}")
    print(f"  Command: {settings['ports']['command']}")
    print(f"  API:     {settings['ports']['api']}")
    print(f"  WebUI:   {settings['ports']['webui']}")
    print(f"  Host:    {settings['host']}")

    await start_servers(settings)


if __name__ == "__main__":
    asyncio.run(main())
