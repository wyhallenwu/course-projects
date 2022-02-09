package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"strings"
)

func ConnectProxy() (net.Conn, error) {
	conn, err := net.Dial("tcp", "127.0.0.1:10000")
	if err != nil {
		fmt.Println("error is: ", err)
	}
	fmt.Println("connected!")
	return conn, err
}

func SendCommand(conn net.Conn) {
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

func ReceiveMessage(conn net.Conn) {
	message := make([]byte, 4096)
	n, err := conn.Read(message)
	if err != nil {
		fmt.Println("ReceiveMessage: ", err)
	}
	fmt.Println(string(message[:n]))
}

func main() {
	conn, err := ConnectProxy()
	if err != nil {
		fmt.Println("connect proxy successfully.")
	}
	SendCommand(conn)
	ReceiveMessage(conn)
	conn.Close()
}
