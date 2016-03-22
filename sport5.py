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
                "clock_background" : "sport blue",
                "clock_font" : "Dosis Bold 24",
                "text_area_head_font" : "Dosis Medium 38",
                "text_area_head_color" : "sport gold",
                "text_area_head_background" : "sport grey 80",
                "text_area_body_font" : "Dosis 28",
                "text_area_body_color" : "white",
            }

    def ticker(self, *args, **kwargs):
        self.cg.nxkit_ticker(*args, **kwargs)

    def clock(self, *args, **kwargs):
        self.cg.nxkit_clock(*args, **kwargs)

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




    def text_area(self, header, text, source=False):
        self.cg.nxkit_text_area(header, text, source)



    def program(self, header, items):
        size=84
        header_size=96
        x, y,  = self.cg.safe("l"), 370
        pad_lft = 25
        pad_rgt = 25
        pad_top = 20
        pad_btm = 20
        spacing = 150
        header_top = 216

        if header:
            self.ctx.set_font_size(header_size)
            tw,th = self.ctx.text_extents(header)[2:4]

            self.set_color("text_background")
            self.rect(x-pad_lft, 216, tw+pad_lft+pad_rgt, th+pad_top+pad_btm)

            self.ctx.move_to(self.SAFEL,header_top+header_size)
            self.set_color("text_head")
            self.ctx.show_text(header)
            self.ctx.stroke()

        self.ctx.set_font_size(size)
        i=-1
        for ts, title in items:
            i+=1
            tw,th = self.ctx.text_extents(title)[2:4]

            self.set_color("sport grey 80")
            self.rect(x-pad_lft, y, 210, 105)
            self.rect(x + 250, y, tw + pad_lft+ pad_rgt, 105)

            self.set_color("text_body")
            self.ctx.move_to(x,y+size)
            self.ctx.show_text(ts)
            self.ctx.stroke()

            self.ctx.move_to(x + 250 + pad_lft, y+size)
            self.ctx.show_text(title)
            self.ctx.stroke()


            y+= spacing


    def crawl(self, text):
        text = textify(text)
        w, h = self.cg.text(text ,
            font=FONT_CRAWL,
            color="text_crawl",
            spacing=0,
            render=False
            )
        top = SAFET + 48
        self.cg.new(w, 1080)
        self.cg.set_color("black glass 75")
        self.cg.rect(0, top, w, 54)
        self.cg.text(text ,
            pos=(0, top+1),
            font=FONT_CRAWL,
            color="text_crawl",
            spacing=0
            )
