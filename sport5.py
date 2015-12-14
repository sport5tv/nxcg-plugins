from nxcg.plugin import NXCGPlugin
from nxcg.utils import textify

SPORT5_COLOR_PRESETS = {
        "sport blue" : "#006CB8",
        "sport blue 80" : "#006CB8E6",
        "sport grey": "#252323",
        "sport grey 80": "#252323E6",
        "text_tick" : "#d3d3d3",
        "text_head" : "#FF8735",
        "text_body" : "#B0C7E8",
        "text_crawl" : "#d3d3d3",
    }

FONT_TICK = 'Roboto Medium 26'
FONT_CLOCK = 'Roboto Bold 26'
FONT_HEAD = 'Roboto Medium 48'
FONT_BODY = 'Roboto 36'
FONT_CRAWL = 'Roboto Medium 26'

FONT_TICK = 'Dosis SemiBold 24'
FONT_CLOCK = 'Dosis Bold 24'
FONT_HEAD = 'Dosis Medium 38'
FONT_BODY = 'Dosis 28'
FONT_CRAWL = 'Dosis Medium 26'

#
# Our TV Plugin itself
#


class Plugin(NXCGPlugin):
    def on_init(self):
        self.cg.colors.update(SPORT5_COLOR_PRESETS)

        self.ticker_voffset = 4 
        self.ticker_h = 48
        self.ticker_y = self.cg.safe("b") - self.ticker_h
        self.clock_w = 100
        self.clock_x = self.cg.safe("r") - self.clock_w
        
    def ticker(self, text):
        text = textify(text)
        text = text.upper()
        self.cg.set_color("sport grey 80")
        self.cg.rect(0, self.ticker_y, self.cg.width, self.ticker_h)
        self.cg.text(text,
                pos=(self.cg.safe("l"), self.ticker_y + self.ticker_voffset),
                color="text_tick",
                font=FONT_TICK,
            )

    def clock(self, tstamp):
        self.cg.set_color("sport blue")
        self.cg.rect(self.clock_x, self.ticker_y, self.cg.width - self.clock_x, self.ticker_h)
        a,b = self.cg.text(tstamp,
                pos=(self.clock_x + 14, self.ticker_y + self.ticker_voffset),
                color="text_tick",
                font=FONT_CLOCK
            )

    def tweet_bar(self, account, text):
        pad_b = 35
        pad_t = 20
        pad_r = 30
        
        tweet_x = self.cg.safe("l")
        tweet_max_w = 1000

        w, h = self.cg.text(text,
            font=FONT_TICK,
            color="text_tick",
            width=tweet_max_w,
            spacing=5,
            render=False
            )

        tweet_bar_w = tweet_x + w + pad_r
        tweet_bar_h = h + pad_b + pad_t

        self.cg.set_color("sport blue 80")
        self.cg.rect(0, self.ticker_y - tweet_bar_h, tweet_bar_w, tweet_bar_h)
        self.cg.text_render(tweet_x,  self.ticker_y - tweet_bar_h + pad_t )


    def info(self, *args):
        base_x = self.cg.safe("l")
        base_y = self.cg.safe("t")
        for i, text in enumerate(args):
            y = base_y + i*(self.ticker_h)
            if i == 0:
                bg_color = "sport blue 80"
                fg_color = "text_tick"
            else:
                bg_color = "sport grey 80"
                fg_color = "text_tick"
           
            w, h = self.cg.text(textify(text),
                font=FONT_TICK,
                color=fg_color,
                render=False
                )

            info_w = base_x + w + 20

            self.cg.set_color(bg_color)
            self.cg.rect(0, y, info_w, self.ticker_h)
            self.cg.text_render(base_x,  y+self.ticker_voffset )




    def text_area(self, header, text, source=False):
        header = textify(header).upper()
        text = textify(text)
        off = 160
        wi = 1200
        pad_h = 20

        ### Header

        x = self.cg.safe("l") 
        y = self.cg.safe("t") + off 

        w, h = self.cg.text(header,
            font=FONT_HEAD,
            color="gold",
            width=wi,
            spacing=0,
            render=False
            )

        self.cg.set_color("sport grey 80")
        self.cg.rect(x-pad_h, y-5, w+(pad_h*2), h+10)
        self.cg.text_render(x, y)

        ### Text

        y = self.cg.safe("t") + off + h + 40
        w, h = self.cg.text(text ,
            font=FONT_BODY,
            color="text_tick",
            width=wi,
            spacing=0,
            render=False
            )

        self.cg.set_color("sport grey 80")
        self.cg.rect(x-pad_h, y-10, w+(pad_h*2), h+100)
        
        
        self.cg.text_render(x, y)



























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
