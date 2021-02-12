import socket
import json

HOST = "localhost"
PORT = 9999

socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_server.bind((HOST, PORT))
socket_server.listen()

if __name__ == "__main__":
    while True:
        print("Waiting connection")
        connection, client_address = socket_server.accept()

        try:
            data = json.dumps(
                {
                    "PROTOCOL": "SAL",
                    "STATE": "WAITING",
                    "message": "From server >>> Connection with Server"
                }
            )
            data = bytes(data, encoding="utf-8")
            connection.send(data)
            print("Connection:", client_address)
        except socket.error:
            print("Fail Connection")
            continue

        while True:
            try:
                data = connection.recv(1024)
                data = json.loads(data.decode("utf-8"))

                if data["STATE"] == "WAITING":
                    print("Respond to", client_address)
                    data = json.dumps(
                        {
                            "PROTOCOL": "SAL",
                            "STATE": "ACTIVE",
                            "message": "From server >>> Success",
                            "link": "google.com/search?q=%s" % data["keyword"]
                        }
                    )
                    connection.send(bytes(data, encoding="utf-8"))

                elif data["STATE"] == "ACTIVE":
                    data = json.dumps(
                        {
                            "PROTOCOL": "SAL",
                            "STATE": "WAITING",
                            "message": "From server >>> Waiting next request from client"
                        }
                    )
                    connection.send(bytes(data, encoding="utf-8"))

                elif data["STATE"] == "CLOSE":
                    data = json.dumps(
                        {
                            "PROTOCOL": "SAL",
                            "STATE": "CLOSE",
                            "message": "From server >>> Disconnect"
                        }
                    )
                    connection.send(bytes(data, encoding="utf-8"))
                    connection.close()
                    print("Disconnect with", client_address)
                    break
            except socket.error:
                connection.close()
                print("Something went wrong from client")
                break
