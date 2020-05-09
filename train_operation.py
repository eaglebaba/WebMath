# import numpy as np
# import pandas as pd
# import cv2
# from os import listdir
# from os.path import isfile, join

# #=================================================================================================#

# # # ### FIRST: RESIZE THE IMAGE

# # mypath = './multiplicationimgs2'
# # target = "*"

# # onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
# # for file in onlyfiles:
# #     img = cv2.imread(f"{mypath}/{file}")
# #     img = cv2.resize(img, (28, 28), interpolation=cv2.INTER_AREA)
# #     cv2.imwrite(f"{mypath}/{file}", img)

# #=================================================================================================#

# # ### CREATE CSV FILE
 
# # all_imgs = np.zeros((1, 784), np.uint8)

# # for file in onlyfiles:
# #     img = cv2.imread(f"{mypath}/{file}", cv2.IMREAD_GRAYSCALE)
# #     img = img.reshape(1, 784)
# #     all_imgs = np.append(all_imgs, img, axis=0)

# # # convert all numbers greater than 0 to 1 to remove complexity of multiple numbers
# # all_imgs = np.where(all_imgs > 0, 1, 0)

# # df = pd.DataFrame(data=all_imgs)
# # df['target'] = target
# # df.to_csv(f"{mypath}/df.csv", index=False)

# #=================================================================================================#

# # ### JOIN ALL DFs TOGETHER
# # df1 = pd.read_csv("./additionimgs2/df.csv")
# # df2 = pd.read_csv("./subtractionimgs2/df.csv")
# # df3 = pd.read_csv("./divisionimgs2/df.csv")
# # df4 = pd.read_csv("./multiplicationimgs2/df.csv")

# # for x in [df1, df2, df3, df4]:
# #     x.drop(labels=[0], inplace=True)

# # df = pd.concat([df1, df2])
# # df = pd.concat([df, df3])
# # df = pd.concat([df, df4])

# # df.to_csv("math_symbols.csv", index=False)

# #=================================================================================================#

# ### TRAIN THE MODEL - done in train_operation.ipynb

x = "2"
y = "+"
z = eval(f"{x}{y}{x}")
print(z)