import json
import socket
import webbrowser

HOST = "localhost"
PORT = 9999

socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if __name__ == "__main__":

    try:
        socket_client.connect((HOST, PORT))
    except socket.error:
        print("Fail connection with server")

    while True:
        try:
            data = socket_client.recv(1024)
            data = json.loads(data.decode("utf-8"))
            print(data["message"])

            if data["STATE"] == "WAITING":
                keyword = input("Keywords you want to find: ")
                if keyword != "":
                    sendto_server = json.dumps(
                        {
                            "PROTOCOL": "SAL",
                            "STATE": "WAITING",
                            "keyword": keyword
                        }
                    )
                    socket_client.send(bytes(sendto_server, encoding="utf-8"))
                else:
                    sendto_server = json.dumps(
                        {
                            "PROTOCOL": "SAL",
                            "STATE": "CLOSE"
                        }
                    )
                    socket_client.send(bytes(sendto_server, encoding="utf-8"))

            elif data["STATE"] == "ACTIVE":
                sendto_server = json.dumps(
                    {
                        "PROTOCOL": "SAL",
                        "STATE": "ACTIVE",
                    }
                )
                webbrowser.open(data["link"])
                socket_client.send(bytes(sendto_server, encoding="utf-8"))

            elif data["STATE"] == "CLOSE":
                socket_client.close()
                break
        except socket.error:
            socket_client.close()
            print("Something went wrong from server")
            break
