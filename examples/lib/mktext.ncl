fun dur col txt => {
  filters = [
    {
      ref = "lavfi",
      name = "color",
      params = {
        c = col,
        s = "1920x1080",
        r = 30,
      },
      duration = dur,
      kind = "video",
    },
    {
      ref = "drawtext",
      text = txt,
      fontcolor = "white",
      fontsize = 96,
      x = "(w - text_w)/2",
      y = "(h - text_h)/2",
    },
  ],
}
