import app.server_http2 as server_http
import app.server_dns as server_dns
import app.wifi_ap as wifi_ap

wifi_ap.init("ESP32_HotSpot")
server_dns.init()
server_http.init()
