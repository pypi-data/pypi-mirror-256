# streamlit_app.py

import streamlit as st
import features
import readrr
#import symmetry
import transformation
#import Sift_keypoints

class ImageFeatureProfiler:
    def __init__(self):
        pass

    def compute_all_features(self, image):
        """
        Compute all features for a given image.

        Parameters:
        - image_path: Path to the input image

        Returns:
        - list: List containing the generated charts.
        """
        sharpness = features.sharpness(image)
        lbp_variance = features.lbpv(image)
        lpq = features.lpq(image)
        fractal_dim = features.fractal_dimension(image)
        textures = features.texture_analysis(image)



def main():
    st.title("Image Feature Profiler")

    # Create an instance of the image feature profiler
    profiler = ImageFeatureProfiler()

    # Upload image file
    image_file = st.file_uploader("Upload an image", type=["jpg", "png"])

    if image_file is not None:
        # Display the uploaded image
        st.image(image_file, caption="Uploaded Image", use_column_width=True)

        # Compute features and display charts
        charts = profiler.compute_all_features(image_file)
        for chart in charts:
            st.write(chart)

if __name__ == "__main__":
    main()
