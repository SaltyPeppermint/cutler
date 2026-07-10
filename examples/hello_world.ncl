let mktext = import "lib/mktext.ncl"
in
{
  jobs = [
    {
      outs = ["video"],
      out_filename = "hello_world.mp4",
      chains = {
        video = {
          inputs = ["hello", "world"],
          filters = [
            {
              ref = "concat_xfade",
              transitions = [
                { effect = "pixelize", duration = 0.3 },
              ],
            },
          ],
        },

        hello = mktext 1 "red" "hello",
        world = mktext 1 "blue" "world",
      },
    },
  ],
}
