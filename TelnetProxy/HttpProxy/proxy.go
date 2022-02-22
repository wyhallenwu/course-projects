package main

import (
	"bytes"
	"fmt"
	"io"
	"log"
	"net"
	"net/url"
	"strings"
)

// 判断是否是黑名单里的ip
func IsContain(items []string, item string) bool {
	for _, eachItem := range items {
		if eachItem == item {
			return true
		}
	}
	return false
}


func main() {
	// 设置不能提供服务的ip
	var BlackList = []string{"49.52.99.103",}
	// tcp连接，监听8080端口
	listener, err := net.Listen("tcp", ":8080")
	if err != nil {
		log.Panic(err)
	}
	for {
		client, err := listener.Accept()
		if err != nil {
			log.Panic(err)
		}
		go Handle(client, BlackList)
	}
}

func Handle(client net.Conn, BlackList []string) {
	if client == nil {
		log.Println("client wrong.")
		return
	}
	defer client.Close()
	log.Printf("remote addr: %v\n", client.RemoteAddr())
	log.Printf("addr: %v\n", client.LocalAddr())
	index := strings.Index(client.RemoteAddr().String(), ":")
	if IsContain(BlackList, client.RemoteAddr().String()[:index]) == true{
		client.Close()
		log.Println("dangerous ip")
		return
	}

	// 用来存放客户端数据的缓冲区
	var buf [1024]byte
	//从客户端获取数据
	n, err := client.Read(buf[:])
	if err != nil {
		log.Println(err)
		return
	}

	if n > 0 {
		log.Println(string(buf[:n]))
	}

	var method, URL, address string
	// 从客户端数据读入method，url
	fmt.Sscanf(string(buf[:bytes.IndexByte(buf[:], '\n')]), "%s%s", &method, &URL)
	hostPortURL, err := url.Parse(URL)
	if err != nil {
		log.Println(err)
		return
	}

	// 如果方法是CONNECT，则为https协议
	if method == "CONNECT" {
		address = hostPortURL.Scheme + ":" + hostPortURL.Opaque
	} else { //否则为http协议
		address = hostPortURL.Host
		// 如果host不带端口，则默认为80
		if strings.Index(hostPortURL.Host, ":") == -1 { //host不带端口， 默认80
			address = hostPortURL.Host + ":80"
		}
	}

	//获得了请求的host和port，向服务端发起tcp连接
	server, err := net.Dial("tcp", address)
	if err != nil {
		log.Println(err)
		return
	}
	//如果使用https协议，需先向客户端表示连接建立完毕
	if method == "CONNECT" {
		fmt.Fprint(client, "HTTP/1.1 200 Connection established\r\n\r\n")
	} else { //如果使用http协议，需将从客户端得到的http请求转发给服务端
		server.Write(buf[:n])
	}

	go io.Copy(server, client)
	io.Copy(client, server)
}
