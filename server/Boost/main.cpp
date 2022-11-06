#include <boost/beast/core.hpp>
#include <boost/beast/websocket.hpp>
#include <opencv2/opencv.hpp>
#include <iostream>
#include <memory>
#include <string>

#include "ImageProcessor.h"

namespace beast = boost::beast;         // from <boost/beast.hpp>
namespace http = beast::http;           // from <boost/beast/http.hpp>
namespace websocket = beast::websocket; // from <boost/beast/websocket.hpp>
namespace net = boost::asio;            // from <boost/asio.hpp>
using tcp = boost::asio::ip::tcp;       // from <boost/asio/ip/tcp.hpp>

class EchoWebsocket : public std::enable_shared_from_this<EchoWebsocket>
{
    websocket::stream<beast::tcp_stream> ws;
    beast::flat_buffer buffer;

    ImageProcessor processor;
    int counter = 0;


public:

    EchoWebsocket(tcp::socket&& socket)
        : ws(std::move(socket))
    {
    }

    void run()
    {
        ws.async_accept(
            [self{shared_from_this()}](beast::error_code ec){

                // if(ec){ std::cout << ec.message() << "\n"; return;}

                self->echo();
            });  
    }

    void onClose() {
        std::cout << "Started nn" << std::endl;
        processor.nearestNeighbour();
        std::cout << "Finished nn" << std::endl;
    }

    void echo()
    {
        
            ws.async_read(
            buffer,
            [self{shared_from_this()}, this](beast::error_code ec, std::size_t bytes_transferred)
            {
                if(ec == websocket::error::closed) {
                    self->onClose();
                    return;
                }
                    

                std::cout << "new message: " << counter++ << std::endl;

                if(ec){ 
                    std::cout << "Error: " << ec.message() << "\n"; 
                    self->onClose();
                    return;}

                auto out = beast::buffers_to_string(self->buffer.cdata());
                self->buffer.consume(self->buffer.size());
                // std::cout << out << std::endl;
                processor.processMessage(out);
                // processor.writeMask("./test.png");
                self->echo();

                // self->ws.async_write(
                //      self->buffer.data(),
                //      [self](beast::error_code ec, std::size_t bytes_transferred)
                //      {

                //         if(ec){ std::cout << ec.message() << "\n"; return;}

                //         self->buffer.consume(self->buffer.size());

                //         self->echo();
                //      });
            });
    }

};

class Listener : public std::enable_shared_from_this<Listener>
{
    net::io_context& ioc;
    tcp::acceptor acceptor;

public:
    Listener(
        net::io_context& ioc,
        unsigned short int port
        )
        : ioc(ioc)
        , acceptor(ioc, {net::ip::make_address("127.0.0.1"), port}){
            std::cout << "Started listening" << std::endl;
        }

    void asyncAccept()
    {
        acceptor.async_accept(
            ioc,
            [self{shared_from_this()}](boost::system::error_code ec, tcp::socket socket) {

                std::cout << "New connection" << std::endl;
                
                std::make_shared<EchoWebsocket>(std::move(socket))->run();

                self->asyncAccept();
                });
    }

};

int main(int argc, char* argv[])
{

    auto const port = 8083;
    net::io_context ioc{};

    std::make_shared<Listener>(ioc,port)->asyncAccept();

    ioc.run();

    return 0;
}