package main

import (
	"fmt"
	"net"
)

const proxy_addr string = "58.199.162.167"
const server_addr string = "124.70.142.89"

func ConnectServer(ServerAddr string) net.Conn {
	conn, err := net.Dial("tcp", fmt.Sprintf("%s:10000", ServerAddr))
	if err != nil {
		fmt.Println("error is(server ConnectServer): ", err)
	}
	fmt.Println("connected server!")
	return conn
}

func ConfirmConnection() (net.Conn, net.Listener) {
	listener, err := net.Listen("tcp", fmt.Sprintf("%s:10000", proxy_addr))
	if err != nil {
		fmt.Printf("listening false. Fault: %v \n", err)
	}
	fmt.Println("waiting for client connection...")

	conn, err := listener.Accept()
	if err != nil {
		fmt.Printf("listening false. Fault: %v \n", err)
	}
	// fmt.Println("connection from ", conn.RemoteAddr())
	fmt.Println("connected clinet.")
	return conn, listener
}

func ReceiveCommand(conn net.Conn, listener net.Listener) string {
	result := make([]byte, 4096)
	n, err := conn.Read(result)
	if err != nil {
		fmt.Println("error is(ReceiveCommand): ", err)
	}
	command := string(result[:n])
	return command
}

func ResendCommand(serverConn net.Conn, command string) {
	serverConn.Write([]byte(command))
}

func ReceiveServer(serverConn net.Conn) string {
	message := make([]byte, 4096)
	n, err := serverConn.Read(message)
	if err != nil {
		fmt.Println("error is(ReceiveServer): ", err)
	}
	return string(message[:n])
}

func SendBack(message string, clientConn net.Conn) {
	clientConn.Write([]byte(message))
}

func Vertify(username string, passwd string) bool {
	userinfo := make(map[string]string)
	userinfo["wuyuheng"] = "wuyuheng"
	password, ok := userinfo[username]
	if ok {
		if passwd == password {
			return true
		}
	}
	return false
}

func Check(clientConn net.Conn) bool {
	message := "Please input your username: "
	clientConn.Write([]byte(message))
	username_ := make([]byte, 1024)
	namelen, _ := clientConn.Read(username_)
	username := string(username_[:namelen])
	message = "Please input your password: "
	clientConn.Write([]byte(message))
	password_ := make([]byte, 1024)
	passlen, _ := clientConn.Read(password_)
	password := string(password_[:passlen])
	if Vertify(username, password) {
		message = "success"
		clientConn.Write([]byte(message))
		return true
	} else {
		message = "false"
		clientConn.Write([]byte(message))
		return false
	}

}

func GetServerAddr(clientConn net.Conn) string {
	ServerAddr := make([]byte, 1024)
	n, _ := clientConn.Read(ServerAddr)
	if string(ServerAddr[:n]) != server_addr {
		message := "false"
		clientConn.Write([]byte(message))
		return message
	} else {
		message := "success"
		clientConn.Write([]byte(message))
		return string(ServerAddr[:n])
	}

}

func main() {
	for {
		clientConn, clientListener := ConfirmConnection()
		success := Check(clientConn)
		if !success {
			message := "Wrong Try Again."
			clientConn.Write([]byte(message))
			clientListener.Close()
			clientConn.Close()
			continue
		}
		ServerAddr := GetServerAddr(clientConn)
		if ServerAddr == "false" {
			clientListener.Close()
			clientConn.Close()
			fmt.Println("try again")
			continue
		}
		serverConn := ConnectServer(ServerAddr)
		for {
			command := ReceiveCommand(clientConn, clientListener)
			fmt.Println(command)
			ResendCommand(serverConn, command)
			result := ReceiveServer(serverConn)
			if command == "quit telnet" {
				clientConn.Close()
				clientListener.Close()
				serverConn.Close()
				break
			}
			fmt.Println(result)
			SendBack(result, clientConn)
			fmt.Println("end process")
		}
	}
}
