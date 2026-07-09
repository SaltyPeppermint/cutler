let
  mktext = import "lib/mktext.ncl"
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
    },
  ],
}
