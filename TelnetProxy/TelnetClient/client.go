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

func Check(conn net.Conn) bool {
	message := make([]byte, 1024)
	conn.Read(message)
	fmt.Println(string(message))
	reader := bufio.NewReader(os.Stdin)
	username, _ := reader.ReadString('\n')
	username = strings.TrimSuffix(username, "\n")
	conn.Write([]byte(username))
	conn.Read(message)
	fmt.Println(string(message))
	reader2 := bufio.NewReader(os.Stdin)
	password, _ := reader2.ReadString('\n')
	password = strings.TrimSuffix(password, "\n")
	conn.Write([]byte(password))

	n, _ := conn.Read(message)
	if string(message[:n]) == "success" {
		fmt.Println("log in success!")
		return true
	} else {
		conn.Close()
		return false
	}
}

func ServerAddr(conn net.Conn) bool {
	fmt.Printf("Please input server address: ")
	reader := bufio.NewReader(os.Stdin)
	ServerAddr, _ := reader.ReadString('\n')
	ServerAddr = strings.TrimSuffix(ServerAddr, "\n")
	conn.Write([]byte(ServerAddr))

	message := make([]byte, 1024)
	n, _ := conn.Read(message)
	return string(message[:n]) != "false"
}

func main() {
	conn, _ := ConnectProxy()
	if !Check(conn) {
		fmt.Println("Wrong. Please try again.")
		return
	}
	if !ServerAddr(conn) {
		fmt.Println("Cannot connected.")
		return
	}
	fmt.Println("connected ")
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
