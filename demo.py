import time
import asyncio
from bilibili_live import live

roomid = 房间号
room = live.RoomCollection(roomid=roomid)
room_operation = live.RoomOperation(roomid=roomid)
bulletchat = live.BulletChat(msg="弹幕测试")
cookies = live.Cookies(sessdata="",
                       buvid3="",
                       bili_jct="")


@room.on("DANMU_MSG")
async def on_danmu(msg):
    uname = msg['info'][2][1]
    text = msg['info'][1]
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg['info'][9]['ts']))
    print('[danmu]' + 'time:' + localtime + ' ' + uname + ':' + text)


@room.on("SEND_GIFT")
async def on_gift(msg):
    uname = msg['data']['uname']
    gift_num = str(msg['data']['num'])
    act = msg['data']['action']
    gift_name = msg['data']['giftName']
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg['data']['timestamp']))
    print('[gift]' + 'time:' + localtime + ' ' + uname + ' ' + act + ' ' + gift_num + ' ' + gift_name)
    # 礼物回复答谢
    bulletchat.msg = "感谢 " + uname + " " + act + "的" + gift_num + "个" + gift_name
    await room_operation.send_bulletchat(bulletchat=bulletchat, cookies=cookies)


@room.on("COMBO_SEND")
async def on_gifts(msg):
    uname = msg['data']['uname']
    gift_num = str(msg['data']['combo_num'])
    act = msg['data']['action']
    gift_name = msg['data']['gift_name']
    print('[combo_gift]' + uname + ' ' + act + ' ' + gift_num + ' ' + gift_name)


@room.on("INTERACT_WORD")
async def on_welcome(msg):
    uname = msg['data']['uname']
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg['data']['timestamp']))
    if msg['data']['msg_type'] == 2:
        print('[people]' + 'time:' + localtime + ' ' + uname + ' ' + '关注了直播间')
    else:
        print('[people]' + 'time:' + localtime + ' ' + uname + ' ' + '进入直播间')


@room.on("ENTRY_EFFECT")
async def on_welcome_2(msg):
    uname = msg['data']['copy_writing'].split('<%')[1].split('%>')[0]
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg['data']['trigger_time'] / 1000000000 ))
    print('[people]高能榜' + 'time:' + localtime + ' ' + uname + ' ' + '进入直播间')


if __name__ == '__main__':
    remote = 'wss://broadcastlv.chat.bilibili.com:443/sub'
    try:
        asyncio.get_event_loop().run_until_complete(room.startup(uri=remote))
    except Exception as exc:
        print("Error:", exc)
