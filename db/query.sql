# 4.各种查询
# 4.1
# 找出全站点击数前10的帖子 #返回它们的post_ids以及对应的点击数
SELECT post_id,post_clickcnt FROM posts ORDER BY post_clickcnt DESC LIMIT 10;
# 找出全站回复数前10的帖子 #返回它们的post_ids以及对应的回复数
SELECT reply_mainpostid,COUNT(reply_mainpostid) FROM reply GROUP BY reply_mainpostid ORDER BY COUNT(reply_mainpostid) DESC LIMIT 10;


# 4.2
# 按照板块查找在此板块发过贴的用户及其基本信息 # 以下语句以board_id=0为例 可以简单换成其他值
SELECT users.user_id,users.user_name,users.user_birthday,users.user_gender,users.user_level FROM users WHERE users.user_id IN (SELECT DISTINCT posts.user_id FROM posts WHERE posts.board_id = 0);
# 按照版块查找在此版块发过贴的用户及其基本信息，并按照发帖总数排序 # 以下语句以board_id=0为例
SELECT posts.user_id,COUNT(posts.post_id),users.user_name,users.user_gender FROM posts,users WHERE posts.user_id = users.user_id GROUP BY posts.user_id ORDER BY COUNT(posts.post_id) DESC;
# 按照版块查找在此版块回过贴的用户及其基本信息，并按照回帖总数排序 # 一下语句以board_id=0为例 可将'IN'前的数字替换为其他board_id
SELECT reply.user_id,COUNT(reply.reply_id),users.user_name,users.user_gender,users.user_birthday FROM reply,users WHERE reply.user_id = users.user_id AND 0 IN (SELECT posts.board_id FROM posts WHERE posts.post_id = reply.reply_mainpostid) GROUP BY reply.user_id ORDER BY COUNT(reply.reply_id) DESC;


# 4.3
# 先建立视图 
#board_id 可以改成任意一个board的board_id
# 如果视图已经存在 先删除它 
# DROP VIEW tempview;
CREATE VIEW tempview AS (SELECT posts.post_id, reply.reply_id, (reply.reply_time - posts.post_time) AS hotscore FROM posts, reply WHERE posts.post_id = reply.reply_mainpostid AND posts.board_id = 0 );
# 找到有最大热度的post的id
SELECT post_id FROM tempview ORDER BY hotscore DESC LIMIT 1;
# 查询得到回复了此post的所有用户的user_name和user_id
SELECT DISTINCT users.user_name,reply.user_id FROM users, reply WHERE reply.user_id = users.user_id AND reply.reply_mainpostid IN (SELECT post_id FROM tempview WHERE hotscore IN(SELECT MAX(tv.hotscore) FROM tempview AS tv));
# 查询结束删除视图
DROP VIEW tempview;


# 4.4
# 对于每个版块找出点击数大于平均点击数的帖子 #以下查询的board_id可以改为任意一个board的board_id
SELECT posts.post_id FROM posts WHERE posts.post_clickcnt > all(SELECT AVG(pts.post_clickcnt) FROM posts as pts WHERE pts.board_id =0) AND posts.board_id = 0;
# 找出在该版块中回复数大于 平均回复数的用户 #以下查询的board_id可以改为任意一个board的board_id
#如果视图已经存在就先删除它
# DROP VIEW tempview2;
CREATE VIEW tempview2 AS (SELECT reply.user_id, COUNT(reply.reply_id) AS replyinboard_cnt FROM reply WHERE reply.reply_mainpostid IN (SELECT posts.post_id FROM posts WHERE posts.board_id = 0) GROUP BY reply.user_id ;
SELECT user_id, replyinboard_cnt FROM tempview2 WHERE replyinboard_cnt > ALL (SELECT AVG(tv2.replyinboard_cnt) FROM tempview2 AS tv2);
# 查询结束删除视图
DROP VIEW tempview2;


# 4.5
# 找出在版块A发帖比在版块B中发帖多的所有用户
# 以下查询中的posts.board_id 可换位任意 板块A 的board_id 同理pts.board_id 可换为任意一个 板块B 的board_id
SELECT posts.user_id FROM posts WHERE posts.board_id = 0 GROUP BY posts.user_id HAVING COUNT(posts.post_id) > ALL (SELECT COUNT(pts.post_id) FROM posts as pts WHERE pts.user_id = posts.user_id AND pts.board_id = 1 GROUP BY pts.user_id);