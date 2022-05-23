#include "tcp_receiver.hh"

// Dummy implementation of a TCP receiver

// For Lab 2, please replace with a real implementation that passes the
// automated checks run by `make check_lab2`.

template <typename... Targs>
void DUMMY_CODE(Targs &&.../* unused */) {}

using namespace std;

void TCPReceiver::segment_received(const TCPSegment &seg) {
    // abadon all until _syn received
    if (!_syn_set && !seg.header().syn) {
        return;
    }
    const TCPHeader h = seg.header();
    if (h.syn && !_syn_set) {
        this->_syn_set = true;
        this->_isn = seg.header().seqno;
    }
    // received bytes
    uint64_t abs_ackno = this->stream_out().bytes_written() + 1;
    uint64_t curr_abs_seqno = unwrap(h.seqno, _isn, abs_ackno);

    uint64_t stream_index = curr_abs_seqno - 1 + (h.syn);
    _reassembler.push_substring(seg.payload().copy(), stream_index, h.fin);
}

std::optional<WrappingInt32> TCPReceiver::ackno() const {
    if (!_syn_set) {
        return nullopt;
    }
    uint64_t abs_ackno = _reassembler.stream_out().bytes_written() + 1;
    if (_reassembler.stream_out().input_ended()) {
        ++abs_ackno;
    }
    return WrappingInt32{_isn} + abs_ackno;
}

size_t TCPReceiver::window_size() const { return _capacity - _reassembler.stream_out().buffer_size(); }
