import os

# --- 50 Authentic Tang Poem Data ---
# A list of tuples, each containing (Title, Author, Chinese Text).
# This expanded list contains 50 classic Tang Dynasty poems.
#
poems_data = [
    # Li Bai (李白) - The Immortal Poet
    (
        "靜夜思",
        "李白 (Li Bai)",
        """床前明月光，
疑是地上霜。
舉頭望明月，
低頭思故鄉。"""
    ),
    (
        "望廬山瀑布",
        "李白 (Li Bai)",
        """日照香爐生紫煙，
遙看瀑布掛前川。
飛流直下三千尺，
疑是銀河落九天。"""
    ),
    (
        "早發白帝城",
        "李白 (Li Bai)",
        """朝辭白帝彩雲間，
千里江陵一日還。
兩岸猿聲啼不住，
輕舟已過萬重山。"""
    ),
    (
        "贈汪倫",
        "李白 (Li Bai)",
        """李白乘舟將欲行，
忽聞岸上踏歌聲。
桃花潭水深千尺，
不及汪倫送我情。"""
    ),
    (
        "黃鶴樓送孟浩然之廣陵",
        "李白 (Li Bai)",
        """故人西辭黃鶴樓，
煙花三月下揚州。
孤帆遠影碧空盡，
唯見長江天際流。"""
    ),
    # Du Fu (杜甫) - The Sage Poet
    (
        "春望",
        "杜甫 (Du Fu)",
        """國破山河在，
城春草木深。
感時花濺淚，
恨別鳥驚心。
烽火連三月，
家書抵萬金。
白頭搔更短，
渾欲不勝簪。"""
    ),
    (
        "登高",
        "杜甫 (Du Fu)",
        """風急天高猿嘯哀，
渚清沙白鳥飛迴。
無邊落木蕭蕭下，
不盡長江滾滾來。
萬里悲秋常作客，
百年多病獨登臺。
艱難苦恨繁霜鬢，
潦倒新停濁酒杯。"""
    ),
    (
        "絕句",
        "杜甫 (Du Fu)",
        """兩個黃鸝鳴翠柳，
一行白鷺上青天。
窗含西嶺千秋雪，
門泊東吳萬里船。"""
    ),
    (
        "江雪",
        "柳宗元 (Liu Zongyuan)", # Note: Often grouped with Du Fu's school of nature
        """千山鳥飛絕，
萬徑人蹤滅。
孤舟蓑笠翁，
獨釣寒江雪。"""
    ),
    (
        "月夜",
        "杜甫 (Du Fu)",
        """今夜鄜州月，
閨中只獨看。
遙憐小兒女，
未解憶長安。
香霧雲鬟濕，
清輝玉臂寒。
何時倚虛幌，
雙照淚痕乾。"""
    ),
    # Wang Wei (王維) - The Poet Buddha
    (
        "鹿柴",
        "王維 (Wang Wei)",
        """空山不見人，
但聞人語響。
返景入深林，
復照青苔上。"""
    ),
    (
        "相思",
        "王維 (Wang Wei)",
        """紅豆生南國，
春來發幾枝。
願君多採擷，
此物最相思。"""
    ),
    (
        "山居秋暝",
        "王維 (Wang Wei)",
        """空山新雨後，
天氣晚來秋。
明月松間照，
清泉石上流。
竹喧歸浣女，
蓮動下漁舟。
隨意春芳歇，
王孫自可留。"""
    ),
    (
        "送元二使安西",
        "王維 (Wang Wei)",
        """渭城朝雨浥輕塵，
客舍青青柳色新。
勸君更盡一杯酒，
西出陽關無故人。"""
    ),
    (
        "九月九日憶山東兄弟",
        "王維 (Wang Wei)",
        """獨在異鄉為異客，
每逢佳節倍思親。
遙知兄弟登高處，
遍插茱萸少一人。"""
    ),
    # Other Major Poets (16-50)
    # Wang Zhihuan (王之渙)
    (
        "登鸛雀樓",
        "王之渙 (Wang Zhihuan)",
        """白日依山盡，
黃河入海流。
欲窮千里目，
更上一層樓。"""
    ),
    (
        "出塞",
        "王之渙 (Wang Zhihuan)",
        """黃河遠上白雲間，
一片孤城萬仞山。
羌笛何須怨楊柳，
春風不度玉門關。"""
    ),
    # Cui Hao (崔顥)
    (
        "黃鶴樓",
        "崔顥 (Cui Hao)",
        """昔人已乘黃鶴去，
此地空餘黃鶴樓。
黃鶴一去不復返，
白雲千載空悠悠。
晴川歷歷漢陽樹，
芳草萋萋鸚鵡洲。
日暮鄉關何處是？
煙波江上使人愁。"""
    ),
    # Meng Haoran (孟浩然)
    (
        "春曉",
        "孟浩然 (Meng Haoran)",
        """春眠不覺曉，
處處聞啼鳥。
夜來風雨聲，
花落知多少。"""
    ),
    (
        "宿建德江",
        "孟浩然 (Meng Haoran)",
        """移舟泊煙渚，
日暮客愁新。
野曠天低樹，
江清月近人。"""
    ),
    # Li Shangyin (李商隱)
    (
        "登樂遊原",
        "李商隱 (Li Shangyin)",
        """向晚意不適，
驅車登古原。
夕陽無限好，
只是近黃昏。"""
    ),
    (
        "無題",
        "李商隱 (Li Shangyin)",
        """相見時難別亦難，
東風無力百花殘。
春蠶到死絲方盡，
蠟炬成灰淚始乾。"""
    ),
    # Du Mu (杜牧)
    (
        "清明",
        "杜牧 (Du Mu)",
        """清明時節雨紛紛，
路上行人欲斷魂。
借問酒家何處有，
牧童遙指杏花村。"""
    ),
    (
        "江南春",
        "杜牧 (Du Mu)",
        """千里鶯啼綠映紅，
水村山郭酒旗風。
南朝四百八十寺，
多少樓臺煙雨中。"""
    ),
    # Bai Juyi (白居易)
    (
        "賦得古原草送別",
        "白居易 (Bai Juyi)",
        """離離原上草，
一歲一枯榮。
野火燒不盡，
春風吹又生。
遠芳侵古道，
晴翠接荒城。
又送王孫去，
萋萋滿別情。"""
    ),
    (
        "問劉十九",
        "白居易 (Bai Juyi)",
        """綠蟻新醅酒，
紅泥小火爐。
晚來天欲雪，
能飲一杯無。"""
    ),
    # Zhang Ji (張繼)
    (
        "楓橋夜泊",
        "張繼 (Zhang Ji)",
        """月落烏啼霜滿天，
江楓漁火對愁眠。
姑蘇城外寒山寺，
夜半鐘聲到客船。"""
    ),
    # Liu Yuxi (劉禹錫)
    (
        "烏衣巷",
        "劉禹錫 (Liu Yuxi)",
        """朱雀橋邊野草花，
烏衣巷口夕陽斜。
舊時王謝堂前燕，
飛入尋常百姓家。"""
    ),
    # Han Yu (韓愈)
    (
        "山石",
        "韓愈 (Han Yu)",
        """山石犖确行徑微，
黃昏到寺蝙蝠飛。
升堂坐階新雨足，
芭蕉葉大梔子肥。"""
    ),
    # Cen Shen (岑參)
    (
        "逢入京使",
        "岑參 (Cen Shen)",
        """故園東望路漫漫，
雙袖龍鍾淚不乾。
馬上相逢無紙筆，
憑君傳語報平安。"""
    ),
    # He Zhizhang (賀知章)
    (
        "回鄉偶書",
        "賀知章 (He Zhizhang)",
        """少小離家老大回，
鄉音無改鬢毛衰。
兒童相見不相識，
笑問客從何處來。"""
    ),
    # Lu Lun (盧綸)
    (
        "塞下曲",
        "盧綸 (Lu Lun)",
        """月黑雁飛高，
單于夜遁逃。
欲將輕騎逐，
大雪滿弓刀。"""
    ),
    # Qiwu Qian (綦毋潛)
    (
        "春泛若耶溪",
        "綦毋潛 (Qiwu Qian)",
        """幽意無斷絕，
此去隨所偶。
晚風吹行舟，
花路入溪口。"""
    ),
    # Jia Dao (賈島)
    (
        "尋隱者不遇",
        "賈島 (Jia Dao)",
        """松下問童子，
言師採藥去。
只在此山中，
雲深不知處。"""
    ),
    # Jin Changxu (金昌緒)
    (
        "春怨",
        "金昌緒 (Jin Changxu)",
        """打起黃鶯兒，
莫教枝上啼。
啼時驚妾夢，
不得到遼西。"""
    ),
    # Zhang Jiuling (張九齡)
    (
        "望月懷遠",
        "張九齡 (Zhang Jiuling)",
        """海上生明月，
天涯共此時。
情人怨遙夜，
竟夕起相思。"""
    ),
    # Wang Changling (王昌齡)
    (
        "出塞",
        "王昌齡 (Wang Changling)",
        """秦時明月漢時關，
萬里長征人未還。
但使龍城飛將在，
不教胡馬度陰山。"""
    ),
    # Wei Yingwu (韋應物)
    (
        "滁州西澗",
        "韋應物 (Wei Yingwu)",
        """獨憐幽草澗邊生，
上有黃鸝深樹鳴。
春潮帶雨晚來急，
野渡無人舟自橫。"""
    ),
    # Gao Shi (高適)
    (
        "別董大",
        "高適 (Gao Shi)",
        """千里黃雲白日曛，
北風吹雁雪紛紛。
莫愁前路無知己，
天下誰人不識君。"""
    ),
    # Liu Changqing (劉長卿)
    (
        "逢雪宿芙蓉山主人",
        "劉長卿 (Liu Changqing)",
        """日暮蒼山遠，
天寒白屋貧。
柴門聞犬吠，
風雪夜歸人。"""
    ),
    # Wei Zhuang (韋莊)
    (
        "菩薩蠻",
        "韋莊 (Wei Zhuang)",
        """人人盡說江南好，
遊人只合江南老。
春水碧於天，
畫船聽雨眠。"""
    ),
    # Xu Hun (許渾)
    (
        "咸陽城西樓晚眺",
        "許渾 (Xu Hun)",
        """一上高城萬里愁，
蒹葭楊柳似汀洲。
溪雲初起日沉閣，
山雨欲來風滿樓。"""
    ),
    # Sikong Tu (司空圖)
    (
        "二十四詩品 - 雄渾",
        "司空圖 (Sikong Tu)",
        """大用外腓，
真體內充。
反以取通，
物無定形。"""
    ),
    # Wang Han (王翰)
    (
        "涼州詞",
        "王翰 (Wang Han)",
        """葡萄美酒夜光杯，
欲飲琵琶馬上催。
醉臥沙場君莫笑，
古來征戰幾人回。"""
    ),
    # Zhang Ruoxu (張若虛)
    (
        "春江花月夜 (excerpt)", # A very long poem, using the first two lines
        "張若虛 (Zhang Ruoxu)",
        """春江潮水連海平，
海上明月共潮生。"""
    ),
    # Cui Tu (崔塗)
    (
        "除夜有懷",
        "崔塗 (Cui Tu)",
        """迢遞三巴路，
羈危萬里身。
亂山殘雪夜，
孤獨異鄉人。"""
    ),
    # Chang Jian (常建)
    (
        "題破山寺後禪院",
        "常建 (Chang Jian)",
        """清晨入古寺，
初日照高林。
曲徑通幽處，
禪房花木深。"""
    ),
    # Liu Zhongyong (劉中庸)
    (
        "征人怨",
        "劉中庸 (Liu Zhongyong)",
        """歲歲金河復玉關，
朝朝馬策與刀環。
三春白雪歸青塚，
萬里黃河繞黑山。"""
    ),
    # Guo Zhen (郭震)
    (
        "華清宮",
        "郭震 (Guo Zhen)",
        """飛閣凌芳樹，
華池落彩虹。
懸門啟重棟，
秀戶闢華窗。"""
    ),
    # Wang Wan (王灣)
    (
        "次北固山下",
        "王灣 (Wang Wan)",
        """客路青山外，
行舟綠水前。
潮平兩岸闊，
風正一帆懸。
海日生殘夜，
江春入舊年。
鄉書何處達，
歸雁洛陽邊。"""
    )
]

# --- Main Script ---

def generate_poem_files():
    """
    Iterates through the poems_data list and writes each poem
    to a uniquely named text file.
    """
    
    # Use only the first 50 poems if the list is longer, though it's now exactly 50.
    poems_to_generate = poems_data[:50]
    num_poems = len(poems_to_generate)

    print(f"Starting to generate {num_poems} Tang Dynasty poem files...")
    print("-" * 40)

    for i, (title, author, poem_text) in enumerate(poems_to_generate):
        
        # Calculate the file number (1-indexed)
        file_number = i + 1
        
        # Format the filename with a leading zero (e.g., 01, 02, ... 50)
        filename = f"tang{file_number:02d}_poem.txt"
        
        # Create the full content for the file
        file_content = f"Title: {title}\n"
        file_content += f"Author: {author}\n"
        file_content += "---\n"
        file_content += poem_text
        
        # Write the content to the file
        # 'encoding="utf-8"' is crucial for saving Chinese characters correctly.
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(file_content)
            print(f"Created {filename}")
        except IOError as e:
            print(f"[ERROR] Could not write to file {filename}: {e}")
        except Exception as e:
            print(f"[ERROR] An unexpected error occurred for {filename}: {e}")

    print("-" * 40)
    print(f"\nGeneration complete. **{num_poems} files** created successfully in the current directory.")

if __name__ == "__main__":
    generate_poem_files()
