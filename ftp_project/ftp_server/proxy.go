package proxy

import (
	"fmt"
	"net"
)

const proxy_addr string = "124.70.142.89"

func ConnectServer(ServerAddr string) *net.TCPConn {
	tcpAddr, err := net.ResolveTCPAddr("tcp", fmt.Sprintf("%s:10001", ServerAddr))
	if err != nil {
		fmt.Println("error is(server ConnectServer): ", err)
	}
	conn, err := net.DialTCP("tcp", nil, tcpAddr)
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
	result := make([]byte, 1024)
	n, err := conn.Read(result)
	if err != nil {
		fmt.Println("error is(ReceiveCommand): ", err)
	}
	command := string(result[:n])
	return command
}

func ResendCommand(serverConn *net.TCPConn, command string) {
	serverConn.Write([]byte(command))
}

func ReceiveServer(serverConn *net.TCPConn) string {
	message := make([]byte, 1024)
	n, err := serverConn.Read(message)
	if err != nil {
		fmt.Println("error is(ReceiveServer): ", err)
	}
	return string(message[:n])
}

func SendBack(message string, clientConn net.Conn) {
	clientConn.Write([]byte(message))
}

func Process(ServerAddr string) {
	serverConn := ConnectServer(ServerAddr)
	clientConn, clientListener := ConfirmConnection()
	command := ReceiveCommand(clientConn, clientListener)
	ResendCommand(serverConn, command)
	result := ReceiveServer(serverConn)
	SendBack(result, clientConn)

}
