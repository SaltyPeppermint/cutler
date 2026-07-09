let
  mktext = fun dur col txt => {
    filters = [
      {
        ref = "read_clip",
        filename = "color=c=%{col}:s=1920x1080:r=30",
        fmt = "lavfi",
        duration = dur,
      },
      { ref = "get_video" },
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
in fun { txt } => {
  jobs = [
    {
      outs = ["video", "audio"],
      out_filename = "/tmp/nice.mp4",
      chains = {
        video = {
          inputs = ["txtslide"],
          filters = [
            {
              ref = "concat_xfade",
              transitions = [
              ],
            },
          ],
        },

        audio = {
          inputs = ["silence"],
          filters = [
            {
              ref = "concat_audio_fade",
              transition_durations = [ ],
            },
          ],
        },

        txtslide = mktext 2 "red" txt,

        silence = {
          filters = [
            {
              ref = "read_clip",
              filename = "anullsrc=channel_layout=stereo:sample_rate=48000",
              fmt = "lavfi",
              duration = 2,
            },
            { ref = "get_audio" },
          ],
        },
      },
    },
  ],
}
