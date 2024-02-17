import sys
sys.path.append("E:/projects/Python/git-proj/melobot_renew/")
from melobot.utils.checker import AtChecker
from melobot.models.event import BotEventBuilder


ac = AtChecker()
# e = BotEventBuilder.build('{"time":1707662411,"self_id":1801297943,"post_type":"message","message_type":"group","sub_type":"normal","message_id":112974548,"group_id":174720233,"peer_id":1801297943,"user_id":1574260633,"message":[{"data":{"text":"测试消息"},"type":"text"}],"raw_message":"测试消息","font":0,"sender":{"user_id":1574260633,"nickname":"律回子","card":"律回子","role":"owner","title":"","level":""}}')
e = BotEventBuilder.build('{"time":1707662553,"self_id":1801297943,"post_type":"message","message_type":"group","sub_type":"normal","message_id":495305026,"group_id":174720233,"peer_id":1801297943,"user_id":1574260633,"message":[{"data":{"qq":"1574260633"},"type":"at"},{"data":{"text":" afajfkjalfjl;ajf;la;lf"},"type":"text"}],"raw_message":"[CQ:at,qq=1574260633] afajf[CQ:image,qq=1574260633]kj[CQ:at,qq=157426024324633]alfjl;ajf;la;lf[CQ:at,qq=1574260234234633]","font":0,"sender":{"user_id":1574260633,"nickname":"律回子","card":"律回子","role":"owner","title":"","level":""}}')
print(ac.check(e))