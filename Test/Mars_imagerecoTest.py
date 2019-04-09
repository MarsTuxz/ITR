import Image_reco
if __name__ == '__main__':
        image = Image_reco.Image_rec()
        import os
        path = 'image_test1'
        parents = os.listdir(path)
        print(parents)
        for parent in parents:
                print(parent)

                child = os.path.join(path, parent)
                #img = image.size_change(child)
                text = image.feedbackWord(child)
                print(text)