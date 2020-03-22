
from resources.lib.vier import Vier

username = "opvolger@gmail.com"
password = "***************"

vier = Vier(username, password)

# print(Vier.getRegexEpisodes())

print(vier.getProgrammas())

print(vier.getEpisodes("/expeditie-robinson"))

print(vier.getPlayUrl("https://www.vier.be/video/expeditie-robinson/expeditie-robinson-s7/expeditie-robinson-s7-aflevering-9", "4453a72f-6f91-4734-9b9e-51e45ef26936"))
