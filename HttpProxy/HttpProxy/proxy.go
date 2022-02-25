package main

import (
	"bytes"
	"fmt"
	"io"
	"log"
	"net"
	"net/url"
	"strings"
	"flag"
	// "net/http"
)




func main() {
	// 设置参数 dangerouIp:屏蔽的客户端ip， keyword:屏蔽的服务器站点
	var dangerousIp string
	var keyword string
	flag.StringVar(&dangerousIp, "ip", "", "默认为空")
	flag.StringVar(&keyword, "kw", "none", "默认为空")
	flag.Parse()

	// 设置不能提供服务的ip
	var BlackList = []string{"49.52.99.102",}
	BlackList = append(BlackList, dangerousIp)

	// tcp连接，监听8080端口
	listener, err := net.Listen("tcp", ":8080")
	if err != nil {
		log.Panic(err)
	}
	for {
		client, err := listener.Accept()
		// defer client.Close()
		if err != nil {
			log.Panic(err)
		}
		go Handle(client, BlackList, keyword)
	}
}

func Handle(client net.Conn, BlackList []string, keyword string) {
	if client == nil {
		log.Println("client wrong.")
		return
	}
	defer client.Close()
	// log.Printf("remote addr: %v\n", client.RemoteAddr())
	// log.Printf("addr: %v\n", client.LocalAddr())
	index := strings.Index(client.RemoteAddr().String(), ":")
	if IsContain(BlackList, client.RemoteAddr().String()[:index]) == true{
		Redirect2(client)
		client.Close()
		log.Println("dangerous ip")
		return
	}

	// 用来存放客户端数据的缓冲区
	var buf [4096]byte
	//从客户端获取数据
	n, err := client.Read(buf[:])
	if err != nil {
		log.Println(err)
		return
	}

	// if n > 0 {
	// 	log.Println(string(buf[:n]))
	// }

	// 判断是否是要过滤的站点，是则断开连接
	if Filter(string(buf[:]), keyword) {
		client.Close()
		log.Println("can't access ", keyword)
		return
	}


	// 从客户端数据读入method，url
	var method, URL, address string
	fmt.Sscanf(string(buf[:bytes.IndexByte(buf[:], '\n')]), "%s%s", &method, &URL)
	hostPortURL, err := url.Parse(URL)
	log.Println(hostPortURL)
	if err != nil {
		log.Println(err)
		return
	}

	if IsLocal(hostPortURL.Host) {
		client.Close()
		log.Println("can't access local")
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
			// fmt.Println("**************************")
			// fmt.Println(address)
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

	//传输的内容直接转发
	go io.Copy(server, client)
	io.Copy(client, server)
}


func Redirect1(client net.Conn) {
	fmt.Fprint(client, "HTTP/1.1 301 Moved Permanently\r\n\r\n")
	server, _ := net.Dial("tcp", "www.gov.cn:80")
	defer server.Close()
	msg := strings.Builder{}
	msg.WriteString("GET http://www.gov.cn/ HTTP/1.1\r\n")
	msg.WriteString("Host: www.gov.cn\r\n")
	msg.WriteString("User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0\r\n")
	msg.WriteString("Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8\r\n")
	msg.WriteString("Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2\r\n")
	msg.WriteString("Accept-Encoding: gzip, deflate\r\n")
	msg.WriteString("DNT: 1\r\n")
	msg.WriteString("Connection: keep-alive\r\n")
	// msg.WriteString("Cookie: __asc=85acc12917f2558a84cd0153721; __auc=85acc12917f2558a84cd0153721; wdcid=268dda88f9218613; wdlast=1645600176; wdses=752d5a4670cbb841\r\n")
	msg.WriteString("Upgrade-Insecure-Requests: 1\r\n")
	msg.WriteString("Cache-Control: max-age=0\r\n")
	msg.WriteString("\r\n")
	server.Write([]byte(msg.String()))
	fmt.Println("yes")
	io.Copy(client, server)
}


func Redirect2(client net.Conn) {
	fmt.Fprint(client, "jiuzhe")
}


// 过滤希望屏蔽的站点
func Filter(header string, keyword string) bool {
	if strings.Contains(header, keyword) {
		return true
	}
	return  false
}

// 判断是否是黑名单里的ip
func IsContain(items []string, item string) bool {
	for _, eachItem := range items {
		if eachItem == item {
			return true
		}
	}
	return false
}

// 判断是否是在访问代理服务器，防止攻击
func IsLocal(requestIp string) bool{
	var IpSet = []string{"1.15.176.231", "127.0.0.1"}
	for _, eachIp := range IpSet {
		if requestIp == eachIp {
			return true
		}
	}
	return false
}
