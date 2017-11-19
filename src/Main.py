import PIL.Image
import core.Vector

print(dir(PIL.Image))

newImg = PIL.Image.new("RGBA",(640,640),(0,255,0))
print(dir(newImg))
newImg.save("test.png", "PNG")