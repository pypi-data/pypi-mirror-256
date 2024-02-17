import streamlit as st
import features
import readrr
import matplotlib.pyplot as plt
from Sift_keypoints import visualize_keypoints
def main():

    # st.title("Symmetry Detection App")
    image_path = r"C129.png"
    # st.subheader(f"Mirror Line Graph for {image_path}")
    # fig = bilateral_syemmetry(image_path, "With Mirror Line")
    # st.pyplot(fig)
    st.title("Your Streamlit App")

    # Get the path to the image
    image_path = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    st.write("hettt")
    st.imshow(image_path)
        


if __name__== "_main_":
    main()