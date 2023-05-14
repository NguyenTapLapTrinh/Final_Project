import socket

def get_ip_address():
    # Tạo một socket để kết nối với một địa chỉ IP không tồn tại
    # Điều này giúp lấy địa chỉ IP cục bộ của máy tính
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("10.255.255.255", 1))

    # Lấy địa chỉ IP được gán cho socket
    ip_address = sock.getsockname()[0]

    # Đóng socket
    sock.close()

    return ip_address

# Gọi hàm để lấy địa chỉ IP và in ra màn hình
ip = get_ip_address()
print(type(ip))