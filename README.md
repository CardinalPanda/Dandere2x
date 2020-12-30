<p align="center">
    <img src="https://i.imgur.com/ixiaGqT.jpgg" alt="Dandere2x Logo, Made by Tremeschin" width="200" height="200">
</p>

<h3 align="center">Dandere2x!</h3>
<p align="center">
  A faster way to upscale videos using waifu2x using video compression technology.
  <br>
  <br>
  <a href="https://github.com/aka-katto/dandere2x/wiki/How-Dandere2x-Works/"><strong>Click here to read how Dandere2x works! </strong></a>
  <br>
  <a href="https://www.reddit.com/r/Dandere2x/">Subreddit</a>
  ·
  <a href="https://github.com/aka-katto/dandere2x/releases/tag/2.0">Download</a>
  ·
  <a href="https://www.youtube.com/watch?v=5grmGE5al2A">Tutorial</a>
</p>

# Dandere2x's Motivation and Big Idea 

Waifu2x (https://github.com/nagadomi/waifu2x) is a powerful tool for upscaling anime-styled images to a higher resolution. It does this using a convolutional neural network, which can bring greater visual fidelity to images by removing the noise produced from resolution upscaling or compression.

![Image of a Waifu2x Upscale](https://i.imgur.com/irRaQ07.png)

*Image: An image of lower resolution ( left ) being brought to a higher resolution using waifu2x (right). Source: Wikipedia*


While waifu2x may take 2-4 seconds on a modern graphics card to produce a higher resolution image, this becomes problematic when upscaling frames in a video, as one video-second can take multiple minutes to process. Considering the number of visual redundancies found in anime, having an algorithm to identify these redundancies and recycling them would prove to be an effective time-reducing step to help upscale videos to higher resolutions. Dandere2x does this by applying I-frame and p-frame compression to anime-styled videos to reduce the work needed by the GPU.


![Image of I-Frame Compression](https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/I_P_and_B_frames.svg/1920px-I_P_and_B_frames.svg.png)
*Image: Different compression types being visualized with PacMan. Dandere2x uses P-Frames to speed waifu2x up. Source: Wikipedia*

You can read more about how Dandere2x does this <a href="https://github.com/aka-katto/dandere2x/wiki/How-Dandere2x-Works/"><strong>here. </strong></a>

# Docker Usage

The dandere2x docker is currently working off a branch, but it can used using some of the commands here:

```
docker build .

docker run --rm -it --gpus all -v /dev/dri:/dev/dri -v $PWD:/host [build_number] -p singleprocess -ws ./workspace/ -i /host/yn_moving_480.mkv -o /host/sample_output.mkv
```

Where [build_number] is the build id. Assert that you have `nvidia-container-toolkit` installed on your respective machine in order to correctly utilize the image. 

# Downloads

## The latest version can be found here:

https://github.com/aka-katto/dandere2x/releases/tag/3.0

## Linux

This is a bit undermaintained, but a known working verison is found here: https://www.reddit.com/r/Dandere2x/comments/i9xn56/linux_rerelease_other_announcements/

I'm juggling to get the linux version more reliably maintained. 

# Related Resources

[Video2x](https://github.com/k4yt3x/video2x): A lossless video enlarger/video upscaler achieved with waifu2x.

# Credits

This project relies on the following software and projects.

- waifu2x-caffe
- waifu2x
- ffmpeg
- STB Image
- waifu2x-ncnn-vulkan
- waifu2x-converter-cpp-deadsix 
