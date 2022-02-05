package main

import (
	"fmt"
	"net"
)

func main() {
	fmt.Println("start dialing...")
	conn, err := net.Dial("tcp", "124.70.142.89:21")
	if err != nil {
		fmt.Println("net.Dial err: ", err)
		return
	}
	defer conn.Close()

	fmt.Println("start writing...")
	_, err = conn.Write([]byte("are you ready"))
	if err != nil {
		fmt.Println("conn.Write err: ", err)
		return
	}

	buf := make([]byte, 1024)
	fmt.Println("start reading...")
	n, err := conn.Read(buf)
	if err != nil {
		fmt.Println("conn.Read err: ", err)
		return
	}
	fmt.Println("message from server: ", string(buf[:n]))
}
