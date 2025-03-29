import requests
import asyncio
import time
from douyin_const import ua
from utils.database import get_cursor
from datetime import datetime


async def get_douyin_music():
    """
    获取抖音Top50音乐榜单
    :return:
    """
    url = f"https://api3-normal-c-hl.amemv.com/aweme/v1/chart/music/list/?request_tag_from=rn&chart_id=6853972723954146568" \
          f"&count=100&cursor=0&os_api=22&device_type=MI 9" \
          f"&ssmix=a&manifest_version_code=110101&dpi=240&uuid=262324373952550&app_name=aweme&version_name=11.1.0&ts={round(time.time())}" \
          f"&cpu_support64=false&app_type=normal&ac=wifi&host_abi=armeabi-v7a&update_version_code" \
          f"=11109900&channel=douyinw&_rticket={round(time.time() * 1000)}&device_platform=android&iid=157935741181076" \
          f"&version_code=110100&cdid=02a0dd0b-7ed3-4bb4-9238-21b38ee513b2&openudid=af450515be7790d1&device_id=3166182763934663" \
          f"&resolution=720*1280&os_version=5.1.1&language=zh&device_brand=Xiaomi&aid=1128&mcc_mnc=46007"

    res = requests.get(url, headers={"User-Agent": ua["app"]}).json()
    batch_placeholders = []
    values = []
    keys = ['music_id', 'music_title', 'author', 'album', 'cover_hd', 'cover_large', 'cover_medium', 'cover_thumb', 'play_url', 'duration', 'user_count', 'owner_nickname', 'lyric_url', 'song_id',
            'song_title', 'heat', 'created_time']
    insert_key = ", ".join(keys)
    placeholders = ", ".join(["%s"] * len(keys))
    # 获取当前时间
    current_time = datetime.now()
    # 格式化为 yyyy-MM-dd HH:mm:ss
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    print('查询抖音热门歌曲', len(res["music_list"]), '条')
    for i in range(0, len(res["music_list"]) - 1):
        music_item = res["music_list"][i]
        music_info = music_item["music_info"]
        item = (music_info.get('id_str'), music_info.get('title'), music_info.get('author'), music_info.get('album'),
                       music_info.get('cover_hd').get('url_list')[0], music_info.get('cover_large').get('url_list')[0],
                       music_info.get('cover_medium').get('url_list')[0], music_info.get('cover_thumb').get('url_list')[0],
                       music_info.get('play_url').get('url_list')[0], str(music_info.get('duration')), str(music_info.get('user_count')), music_info.get('owner_nickname'),
                       music_info.get('lyric_url', ''), music_info.get('song').get('id_str'), music_info.get('song').get('title'), str(music_item.get('heat')),
                       formatted_time)
        values.append(item)
    sql = f"INSERT INTO t_dy_music_top ({insert_key}) VALUES ({placeholders})"
    print(sql)  # 打印完整 SQL
    cursor = get_cursor()
    cursor.executemany(sql, values)
    print('插入数据成功')

if __name__ == '__main__':
     asyncio.run(get_douyin_music())


