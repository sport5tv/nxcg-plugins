from nxcg.plugin import NXCGPlugin
from nxcg.utils import textify

SPORT5_COLOR_PRESETS = {
        "sport blue"    : "#006CB8",
        "sport blue 80" : "#006CB8E6",
        "sport grey"    : "#252323",
        "sport grey 80" : "#252323E6",
        "sport gold"    : "#ff8735",
    }

#
# Our TV Plugin itself
#

class Plugin(NXCGPlugin):
    def on_init(self):
        self.cg.colors.update(SPORT5_COLOR_PRESETS)
        self.cg.nxkit = {
                "ticker_position" : "bottom",
                "ticker_voffset"  : 4,
                "ticker_background" : "sport grey 80",
                "ticker_color" : "white",
                "ticker_font" : "Dosis SemiBold 24",
                "ticker_caps" : False,
                "clock_background" : "sport blue",
                "clock_font" : "Dosis Bold 24",
                "text_area_head_font" : "Dosis Medium 38",
                "text_area_head_color" : "sport gold",
                "text_area_head_caps" : True,
                "text_area_head_background" : "sport grey 80",
                "text_area_body_font" : "Dosis 28",
                "text_area_body_color" : "white",
            }

    def ticker(self, *args, **kwargs):
        self.cg.nxkit_ticker(*args, **kwargs)

    def clock(self, *args, **kwargs):
        self.cg.nxkit_clock(*args, **kwargs)

    def text_area(self, header, text, source=False):
        self.cg.nxkit_text_area(header, text, source)

    #
    # Sport5 specific widgets
    #

    def tweet_bar(self, account, text):
        pad_b = 35
        pad_t = 20
        pad_r = 30

        tweet_x = self.cg.safe("l")
        tweet_max_w = 1000

        w, h = self.cg.text(text,
            font=self.cg.nxkit["ticker_font"],
            color=self.cg.nxkit["ticker_color"],
            width=tweet_max_w,
            spacing=5,
            render=False
            )

        tweet_bar_w = tweet_x + w + pad_r
        tweet_bar_h = h + pad_b + pad_t

        self.cg.set_color("sport blue 80")
        self.cg.rect(0, self.cg.nxkit_ticker_y - tweet_bar_h, tweet_bar_w, tweet_bar_h)
        self.cg.text_render(tweet_x,  self.cg.nxkit_ticker_y - tweet_bar_h + pad_t )


    def info(self, *args):
        base_x = self.cg.safe("l")
        base_y = self.cg.safe("t")
        for i, text in enumerate(args):
            y = base_y + i*(self.cg.nxkit_param("ticker_height"))
            if i == 0:
                bg_color = "sport blue 80"
                fg_color = "text_tick"
            else:
                bg_color = "sport grey 80"
                fg_color = "text_tick"

            w, h = self.cg.text(textify(text),
                font=self.cg.nxkit["ticker_font"],
                color=fg_color,
                render=False
                )

            info_w = base_x + w + 20

            self.cg.set_color(bg_color)
            self.cg.rect(0, y, info_w, self.cg.nxkit_param("ticker_height"))
            self.cg.text_render(base_x,  y+self.cg.nxkit_param("ticker_voffset"))

