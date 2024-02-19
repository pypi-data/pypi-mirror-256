class CryoImageResults:
    def __init__(self, image, mask_dict):
        self.image = image
        self.bounding_boxes = []
        #self.histograms = []
        self.areas = []
        self.segmentations = []

        for mask in mask_dict: 
            self.bounding_boxes.append(mask['bbox'])
            #self.histograms.append(Utils.generate_histogram(image, mask))
            self.areas.append(mask['area'])
            self.segmentations.append(mask['segmentation'])

