package my_ftp

import (
	"fmt"
	"net"
)

const proxy_addr string = ""

func Listen() bool {
	listener, err := net.Listen("tcp", fmt.Sprintf("%s:21", proxy_addr))
	if err != nil {
		fmt.Printf("listening false. Fault: %v \n", err)
		return false
	}
	fmt.Println("waiting for client connection...")

	conn, err := listener.Accept()
	if err != nil {
		fmt.Printf("listening false. Fault: %v \n", err)
		return false
	}
	fmt.Println("connection from ", conn.RemoteAddr())
	// fmt.Println("connected.")

	for {
		buf := make([]byte, 1024)
		n, err := conn.Read(buf)
		if err != nil {
			fmt.Printf("listening false. Fault: %v \n", err)
			return false
		}
		if string(buf[:n]) == "tcp" {
			conn.Write([]byte("successfully connected."))
		}
		fmt.Println("read message: ", string(buf[:n]))
		if string(buf[:n]) == "quit" {
			conn.Close()
			listener.Close()
			break
		}
	}
	return true
}

// 获取可用端口
func GetAvailablePort() (int, error) {
	address, err := net.ResolveTCPAddr("tcp", fmt.Sprintf("%s:0", "0.0.0.0"))
	if err != nil {
		return 0, err
	}

	listener, err := net.ListenTCP("tcp", address)
	if err != nil {
		return 0, err
	}

	defer listener.Close()
	return listener.Addr().(*net.TCPAddr).Port, nil

}

// 判断端口是否可以（未被占用）
func IsPortAvailable(port int) bool {
	address := fmt.Sprintf("%s:%d", "0.0.0.0", port)
	listener, err := net.Listen("tcp", address)
	if err != nil {
		fmt.Printf("port %s is taken: %s", address, err)
		return false
	}

	defer listener.Close()
	return true
}
