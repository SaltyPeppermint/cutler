let mktext = import "lib/mktext.ncl" in
let mkjob = fun { title, link } => {
    outs = ["video", "audio"],
    out_filename = "/tmp/abba_song_%{title}.mp4",
    chains = {
      video = {
        inputs = ["txtslide", "song_video"],
        filters = [
          {
            ref = "concat_xfade",
            transitions = [
              { duration = 0.5 },
            ],
          },
        ],
      },

      audio = {
        inputs = ["silence", "song_audio"],
        filters = [
          {
            ref = "concat_audio_fade",
            transition_durations = [ 0 ],
          },
        ],
      },

      song = {
        filters = [
          {
            ref = "read_clip",
            filename = "/tmp/abba_song_%{title}_raw.webm",
            gen_cmd = [ "yt-dlp", link, "-o", filename ],
            gen_overwrite = false,
          },
        ],
      },

      song_audio = {
        inputs = ["song"],
        filters = [ { ref = "get_audio" } ],
      },

      song_video = {
        inputs = ["song"],
        filters = [
          { ref = "get_video" },
          { ref = "fps", args = [30] },
          { ref = "scale", w = 1920, h = 1080 },
        ],
      },

      txtslide = mktext 2.5 "red" title,

      silence = {
        filters = [
          {
            ref = "lavfi",
            name = "anullsrc",
            params = {
              channel_layout = "stereo",
              sample_rate = 48000,
            },
            duration = 2,
            kind = "audio",
          },
        ],
      },
    },
  }
in
  fun { records } => {
    jobs = std.array.map mkjob records
  }
