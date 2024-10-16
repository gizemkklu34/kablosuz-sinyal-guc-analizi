import subprocess

# Wi-Fi ağlarını tarama fonksiyonu (Windows için)
def wifi_tarama_windows():
    sonuc = subprocess.run(['netsh', 'wlan', 'show', 'network', 'mode=bssid'], capture_output=True, text=True)
    return sonuc.stdout

# 'netsh' komutunun çıktısını işleyerek SSID ve sinyal gücü bilgilerini ayıklama
def parse_netsh_output(output):
    lines = output.split('\n')
    wifi_dict = {}
    
    ssid = None
    for line in lines:
        line = line.strip()
        if "SSID" in line and "BSSID" not in line:
            ssid = line.split(":")[1].strip()
        if "Signal" in line:
            signal = line.split(":")[1].strip().replace('%', '')
            # SSID'yi ve sinyal gücünü ekle veya güncelle
            if ssid:
                signal = int(signal)
                if ssid not in wifi_dict or signal > wifi_dict[ssid]:
                    wifi_dict[ssid] = signal
    
    return wifi_dict

# Wi-Fi ağlarını CMD'ye yazdırma
def sinyal_gucu_yazdir(wifi_dict):
    for ssid, signal in wifi_dict.items():
        print(f"Ağ Adı (SSID): {ssid}, Sinyal Gücü: {signal}%")

# Ana akış
if __name__ == "__main__":
    sonuc = wifi_tarama_windows()  # Wi-Fi ağlarını tara
    wifi_aglari = parse_netsh_output(sonuc)  # Sonuçları işle
    sinyal_gucu_yazdir(wifi_aglari)  # Sonuçları CMD'ye yazdır
