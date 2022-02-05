package main

import (
	"fmt"
	"net"
)

func main() {
	listener, err := net.Listen("tcp", "192.168.0.51:21")
	if err != nil {
		fmt.Printf("listening false. Fault: %v \n", err)
		return
	}

	defer listener.Close()

	fmt.Println("waiting for client connection...")

	conn, err := listener.Accept()
	fmt.Println("blocking after accepted.")
	if err != nil {
		fmt.Printf("listening false. Fault: %v \n", err)
		return
	}
	defer conn.Close()

	fmt.Println("connected.")

	buf := make([]byte, 1024)
	n, err := conn.Read(buf)
	if err != nil {
		fmt.Printf("listening false. Fault: %v \n", err)
		return
	}

	if string(buf[:n]) == "are you ready" {
		conn.Write([]byte("i am ready"))
	}
	fmt.Println("read message: ", string(buf[:n]))
}
