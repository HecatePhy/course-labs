CREATE TRIGGER `wateringMonitor` AFTER INSERT ON `posts`
 FOR EACH ROW BEGIN

DECLARE lastPostTime DATETIME;
DECLARE lastUserID INT;
DECLARE postCount INT DEFAULT 0;
DECLARE alarmMsg VARCHAR(40);
SET lastPostTime = NEW.post_time;
SET lastUserID = NEW.user_id;
SET postCount = (SELECT COUNT(posts.post_id) FROM posts WHERE posts.user_id = lastUserID AND timestampdiff(minute,posts.post_time,lastPostTime) <= 10);
IF postCount >= 10 THEN
SET alarmMsg = CONCAT("user ",lastUserID, " may be watering!");
SIGNAL SQLSTATE 'HY000' SET MESSAGE_TEXT = alarmMsg;
END IF;

END