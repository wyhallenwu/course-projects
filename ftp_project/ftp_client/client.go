package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"strings"
)

func main() {
	conn, err := ConnectProxy()
	if err != nil {
		fmt.Println("connect proxy successfully.")
	}
	SendCommand(conn)
	conn.Close()
}

func ConnectProxy() (*net.TCPConn, error) {
	tcpAddr, err := net.ResolveTCPAddr("tcp", "124.70.142.89:10000")
	if err != nil {
		fmt.Println("error is: ", err)
	}
	conn, err := net.DialTCP("tcp", nil, tcpAddr)
	if err != nil {
		fmt.Println("error is: ", err)
	}
	fmt.Println("connected!")
	return conn, err
}

func SendCommand(conn *net.TCPConn) {
	reader := bufio.NewReader(os.Stdin)
	for {
		fmt.Println("MyTelnet> ")
		cmdString, err := reader.ReadString('\n')
		if err != nil {
			fmt.Fprintln(os.Stderr, err)
		}
		cmdString = strings.TrimSuffix(cmdString, "\n")
		fmt.Println("execute: ", cmdString)
		if cmdString == "qtelnet" {
			fmt.Println("quit MyTelnet")
			break
		}
		conn.Write([]byte(cmdString))
	}
}

func ReceiveMessage(conn *net.TCPConn) {
	message := make([]byte, 4096)
	n, err := conn.Read(message)
	if err != nil {
		fmt.Println("ReceiveMessage: ", err)
	}

	fmt.Println(string(message[:n]))
}
