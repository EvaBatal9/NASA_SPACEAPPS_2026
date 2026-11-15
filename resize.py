import cv2 

for i in range(10):
    for k in range(5):
        image=cv2.imread("Graphics/segmented_map/topology"+str(k)+"x"+str(i)+".png")
        print(image.size)
        width=image.shape[0]//4
        height=image.shape[1]//4
        resized=cv2.resize(image,(width,height))
        cv2.imwrite("Graphics/segmented_map/topology"+str(k)+"x"+str(i)+".png",resized)
