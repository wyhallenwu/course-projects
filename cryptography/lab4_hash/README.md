# README

## step
firstly, build code framework to check valid video result
`video`: videos/6.2.birthday.mp4_download   
`result`: 03c08f4ee0b576fe319338139c045c89c3e8e9409633bea29442e21425006ea8
- [x] test pass
  
then test on another video  
`video`: videos/6.1.intro.mp4_download  
`result`: 5b96aece304a1422224f9a41b228416028f9ba26b0d1058f400200f06a589949

## framework
firstly, split the video into chunks with 1kB. Storing each chunk in a list while reading.  
After that, using reverse() so that we can hash from end to front.   
Finally, hashing each chunk and then append to next chunk until the last chunk. Hashing the last chunk then get result.