let
  mktext = import "lib/mktext.ncl"
in {
  jobs = [
    {
      outs = ["video", "audio"],
      out_filename = "/tmp/nice.mp4",
      chains = {
        video = {
          inputs = ["three", "two", "one", "here", "test_part1", "censor", "test_part2"],
          filters = [
            {
              ref = "concat_xfade",
              transitions = [
                { effect = "slideleft", duration = 0.3 },
                { effect = "slideright", duration = 0.3 },
                { effect = "pixelize", duration = 0.3 },
                { effect = "vertclose", duration = 0.2 },
                { duration = 0 },
                { duration = 0 },
              ],
            },
          ],
        },

        audio = {
          inputs = ["silence", "test_audio"],
          filters = [
            {
              ref = "concat_audio_fade",
              transition_durations = [ 0.2 ],
            },
          ],
        },

        test = {
          filters = [
            {
              ref = "read_clip",
              filename = "/tmp/test_raw.webm",
              gen_cmd = [ "yt-dlp", "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "-o", "/tmp/test_raw.webm" ],
              gen_overwrite = false,
            },
          ],
        },

        test_video = {
          inputs = [ "test" ],
          filters = [
            { ref = "get_video" },
            { ref = "force_fmt", fmt = "yuv420p" },
            { ref = "fps", args = [30] },
            { ref = "scale", w = 1920, h = 1080 },
            { ref = "split", branch_names = ["foo", "bar"] },
          ],
        },

        test_part1 = {
          inputs = [ "test_video.foo" ],
          filters = [
            { ref = "trim", start = 0, end = 8 },
          ],
        },

        test_part2 = {
          inputs = [ "test_video.bar" ],
          filters = [
            { ref = "trim", start = 10 },
          ],
        },

        test_audio = {
          inputs = [ "test" ],
          filters = [
            { ref = "get_audio" },
          ],
        },

        one = mktext 1.3 "red" "one",
        two = mktext 1.3 "green" "two",
        three = mktext 2.3 "blue" "three",
        censor = mktext 2 "cyan" "[censored]",
        here = mktext 1.2 "pink" "here comes \u{72}\u{69}\u{63}\u{6b}",

        silence = {
          filters = [
            {
              ref = "lavfi",
              name = "anullsrc",
              params = {
                channel_layout = "stereo",
                sample_rate = 48000,
              },
              duration = 1 + 1 + 2 + 1 + 0.2,
              kind = "audio",
            },
          ],
        },
      },
    },
  ],
}
