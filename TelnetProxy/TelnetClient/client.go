package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"strings"
)

func ConnectProxy() (net.Conn, error) {
	conn, err := net.Dial("tcp", "58.199.162.167:10000")
	if err != nil {
		fmt.Println("error is: ", err)
	}
	fmt.Println("connected proxy!")
	return conn, err
}

func SendCommand(conn net.Conn) bool {
	reader := bufio.NewReader(os.Stdin)
	flag := false
	fmt.Printf("\nMyTelnet> ")
	cmdString, err := reader.ReadString('\n')
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
	}
	cmdString = strings.TrimSuffix(cmdString, "\n")
	if cmdString == "quit telnet" {
		flag = true
	}
	// fmt.Println("execute: ", cmdString)
	conn.Write([]byte(cmdString))
	return flag
}

func ReceiveMessage(conn net.Conn) string {
	message := make([]byte, 4096)
	n, _ := conn.Read(message)
	// if err != nil {
	// 	fmt.Println("ReceiveMessage: ", err)
	// }
	// fmt.Println(string(message[:n]))
	return string(message[:n])
}

func main() {
	conn, err := ConnectProxy()
	if err != nil {
		fmt.Println("error is(main): ", err)
	}
	for {
		flag := SendCommand(conn)
		message := ReceiveMessage(conn)
		if flag {
			conn.Close()
			break
		}
		fmt.Printf("%s", message)
	}
}
