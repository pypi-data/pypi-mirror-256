from segment_anything import SamAutomaticMaskGenerator, SamPredictor, sam_model_registry
import numpy as np
import cv2
import  matplotlib.pyplot as plt

class CryoImageResults:
    def __init__(self, image, mask_dict):
        self.image = image
        self.bounding_boxes = []
        self.histograms = []
        self.areas = []
        self.segmentations = []

        for mask in mask_dict: 
            self.bounding_boxes.append(mask['bbox'])
            #self.histograms.append(Utils.generate_histogram(image, mask))
            self.areas.append(mask['area'])
            self.segmentations.append(mask['segmentation'])

class Utils:
    #todo
    @staticmethod
    def generate_histogram(image = [], mask = []):
        if len(image) == 0 or  len(mask) == 0:
            return None
        
        return np.histogram(image, bins=256, range=(0, 256), weights=mask)

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        hist = dict()
        segment = mask['segmentation']
        for i in range(len(segment)):
            for j in range(len(segment[0])):
                if segment[i][j] == True:
                    intensity = gray_image[i][j]
                    hist[intensity] = hist.get(intensity, 0) + 1
        return hist
    
    #todo
    @staticmethod
    def show_boxes(boxs, ax):
        for box in boxs:
            x0, y0 = box[0], box[1]
            w, h = box[2], box[3]
            ax.add_patch(plt.Rectangle((x0, y0), w, h, edgecolor='green', facecolor=(0,0,0,0), lw=1))

    #todo
    @staticmethod
    def visualize_detections(results: CryoImageResults, image, box_prompts = None, point_prompts = None, 
                          see_boxes = True, seepoint_prompts = None, see_masks = False, see_box_prompts = None):
        # if image_scale_percent != 100:
        #     width = int(image.shape[1] * image_scale_percent / 100)
        #     height = int(image.shape[0] * image_scale_percent / 100)
        #     dim = (width, height)
        #     image = cv2.resize(image, dim)

        fig, ax = plt.subplots(1, 2, figsize=(10, 5))
        ax[0].imshow(image)
        ax[1].imshow(image)

        if see_masks:
            Utils.show_masks(results.segmentations, ax[1])
        
        if see_boxes:
            Utils.show_boxes(results.bounding_boxes, ax[1])
            
        #todo add support for prompts
        plt.show()
        return None
    
    #todo
    @staticmethod
    def show_masks(masks, axes=None):
     if axes:
        ax = axes
     else:
        ax = plt.gca()
        ax.set_autoscale_on(False)
     sorted_result = sorted(masks, key=(lambda x: x['area']), reverse=True)
     # Plot for each segment area
     for val in sorted_result:
        mask = val['segmentation']
        img = np.ones((mask.shape[0], mask.shape[1], 3))

        color_mask = np.random.random((1, 3)).tolist()[0]
        for i in range(3):
            img[:,:,i] = color_mask[i]
            ax.imshow(np.dstack((img, mask*0.3)))

class Csam:
    def __init__(self, model_name, model_checkpoint, device = "cuda"):
        self.model = model_name
        self.checkpoint = model_checkpoint
        self.device = device

        self.__load_model()

    def __load_model(self):
        sam = sam_model_registry[self.model](checkpoint = self.checkpoint)
        sam.to(self.device)

        self.mask_generator = SamAutomaticMaskGenerator(sam)
        self.predictor = SamPredictor(sam)   

    def square_finder(self, image, point_prompts = None, box_prompts = None):
        if not box_prompts or point_prompts:
            masks = self.mask_generator.generate(image)
            results = CryoImageResults(image, masks)
        #todo add support for prompts
        return results
    
    def hole_finder(self, image, point_prompts = None, box_prompts = None):
        if not box_prompts or point_prompts:
            masks = self.mask_generator.generate(image)
            results = CryoImageResults(image, masks)
        #todo add support for prompts
        return results

    