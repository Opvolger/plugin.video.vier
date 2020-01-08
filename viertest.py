
from resources.lib.vier import Vier

vier = Vier()

print(Vier.getRegexEpisodes())

print(vier.getProgrammas())

print(vier.getEpisodes("/expeditie-robinson"))

print(vier.getPlayUrl("/video/expeditie-robinson/kandidaat-niels-ik-kijk-er-naar-uit-om-die-nederlanders-kapot-te-maken"))
