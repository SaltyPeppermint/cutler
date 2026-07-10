## cutler

Write declarative recipes to render/cut/stitch/transform video and audio:
yet another builder for ffmpeg filters, tailored to a specific usecase.

#### cutler is declarative
- define recipes in [nickel](https://nickel-lang.org)
- each recipe defines one or more jobs that are rendered with ffmpeg
- jobs are composed of filter chains
- the first filter in each chain may have any number of inputs. All other filters must have 1 input.

#### cutler is powerful
- custom filter generators like `concat_xfade` that run ffprobe on their
  inputs, calculate transition offsets correctly and construct the proper
  ffmpeg filter chain
- instruct the recipe to run arbitrary scripts that generate input videos

#### cutler is lazy
- only runs commands if the final output depends on them being run

#### cutler is eagerly parallel
- all command runs are handled asynchronously
- all processes like ffmpegs, ffprobes, input generators are queued in the same
  pool: cutler doesn't stand around waiting

#### cutler likes data
- pass data from CSV or json to cutler recipes
- emit an ffmpeg job for every CSV line, or do a single stitched render that
  reads its inputs from CSV in one pass
