import requests
from bs4 import BeautifulSoup
from typing import List, Dict

class GoldPriceTracker:
    def __init__(self):
        self.url = "https://giavang.pnj.com.vn/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive"
        }
        self.KHU_VUC_ORDER = ["TPHCM", "Hà Nội", "Miền Tây", "Đông Nam Bộ"]
        self.LOAI_VANG_ORDER = ["SJC", "PNJ"]

    def fetch_gold_prices(self) -> List[Dict]:
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', {'width': '100%', 'border': '1'})
            if not table:
                raise Exception("Không tìm thấy bảng giá vàng")

            temp_data = {kv: {lv: None for lv in self.LOAI_VANG_ORDER} for kv in self.KHU_VUC_ORDER}
            current_region = None

            for row in table.find_all('tr')[1:]:
                cells = row.find_all('td')
                region_cell = row.find('td', {'rowspan': True})

                if region_cell:
                    current_region = region_cell.text.strip()

                if current_region in self.KHU_VUC_ORDER and len(cells) >= 4:
                    gold_type = cells[-4].text.strip()

                    if "SJC" in gold_type:
                        vang_type = "SJC"
                    elif "PNJ" in gold_type:
                        vang_type = "PNJ"
                    else:
                        continue

                    temp_data[current_region][vang_type] = {
                        "gia_mua": cells[-3].text.strip(),
                        "gia_ban": cells[-2].text.strip(),
                        "cap_nhat": cells[-1].text.strip()
                    }

            gold_data = []
            for khu_vuc in self.KHU_VUC_ORDER:
                for loai_vang in self.LOAI_VANG_ORDER:
                    if temp_data[khu_vuc][loai_vang]:
                        data = {
                            "khu_vuc": khu_vuc,
                            "loai_vang": loai_vang,
                            "gia_mua": temp_data[khu_vuc][loai_vang]["gia_mua"],
                            "gia_ban": temp_data[khu_vuc][loai_vang]["gia_ban"],
                            "cap_nhat": temp_data[khu_vuc][loai_vang]["cap_nhat"]
                        }
                        gold_data.append(data)

            return gold_data
        except Exception as e:
            raise Exception(f"⚠️ Lỗi khi lấy giá vàng: {str(e)}")

    def format_gold_prices(self, gold_data: List[Dict]) -> str:
        message = "🏆 *CẬP NHẬT GIÁ VÀNG HÔM NAY* 🏆\n\n"

        region_icons = {
            "TPHCM": "🌆", "Hà Nội": "🏙", "Miền Tây": "🌿", "Đông Nam Bộ": "🌅"
        }
        gold_icons = {
            "SJC": "💛", "PNJ": "💎"
        }

        for khu_vuc in self.KHU_VUC_ORDER:
            region_data = [d for d in gold_data if d["khu_vuc"] == khu_vuc]
            if region_data:
                message += f"{region_icons.get(khu_vuc, '📍')} *{khu_vuc}*\n"
                for data in region_data:
                    message += (
                        f"  {gold_icons.get(data['loai_vang'], '🪙')} *{data['loai_vang']}*\n"
                        f"    🔹 _Mua:_ `{data['gia_mua']} VNĐ`\n"
                        f"    🔹 _Bán:_ `{data['gia_ban']} VNĐ`\n"
                    )
                message += "──────────────\n"

        if gold_data:
            message += f"⏳ *Cập nhật:* `{gold_data[0]['cap_nhat']}`"

        return message

