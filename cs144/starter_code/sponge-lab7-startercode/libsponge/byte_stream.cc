#include "byte_stream.hh"

// Dummy implementation of a flow-controlled in-memory byte stream.

// For Lab 0, please replace with a real implementation that passes the
// automated checks run by `make check_lab0`.

// You will need to add private members to the class declaration in `byte_stream.hh`

template <typename... Targs>
void DUMMY_CODE(Targs &&... /* unused */) {}

using namespace std;

ByteStream::ByteStream(const size_t capacity) : _capacity(capacity) {}

size_t ByteStream::write(const string &data) {
    size_t length = data.length();
    if (length > this->remaining_capacity())
        length = this->remaining_capacity();
    this->_write_bytes_num += length;
    for (size_t i = 0; i < length; ++i) {
        this->_buffer.push_back(data.at(i));
    }
    return length;
}

//! \param[in] len bytes will be copied from the output side of the buffer
string ByteStream::peek_output(const size_t len) const {
    size_t length = len;
    if (length > this->_buffer.size()) {
        length = this->_buffer.size();
    }
    return string().assign(this->_buffer.cbegin(), this->_buffer.cbegin() + length);
}

//! \param[in] len bytes will be removed from the output side of the buffer
void ByteStream::pop_output(const size_t len) {
    if (buffer_empty()) {
        return;
    }
    size_t length = len;
    if (len > this->_buffer.size()) {
        length = this->_buffer.size();
    }
    this->_read_bytes_num += length;
    this->_buffer.erase(this->_buffer.begin(), this->_buffer.begin() + length);
}

//! Read (i.e., copy and then pop) the next "len" bytes of the stream
//! \param[in] len bytes will be popped and returned
//! \returns a string
std::string ByteStream::read(const size_t len) {
    string result = this->peek_output(len);
    this->pop_output(len);
    return result;
}

void ByteStream::end_input() { this->_input_end_flag = true; }

bool ByteStream::input_ended() const { return this->_input_end_flag; }

size_t ByteStream::buffer_size() const { return this->_buffer.size(); }

bool ByteStream::buffer_empty() const { return _buffer.empty(); }

bool ByteStream::eof() const { return buffer_empty() && input_ended(); }

size_t ByteStream::bytes_written() const { return this->_write_bytes_num; }

size_t ByteStream::bytes_read() const { return this->_read_bytes_num; }

size_t ByteStream::remaining_capacity() const { return this->_capacity - this->_buffer.size(); }
