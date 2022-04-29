import streamlit as st
from gen_images import generate_images
from PIL import Image


pkl_dict = {"Animal": "https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan3/"
                      "versions/1/files/stylegan3-r-afhqv2-512x512.pkl",
            "Human": "https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan3/"
                     "versions/1/files/stylegan3-r-ffhq-1024x1024.pkl",
            "Painting": "https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan3/"
                        "versions/1/files/stylegan3-r-metfaces-1024x1024.pkl"}


def encode(name):
    m_bytes = name.encode("utf-8")
    m_int = int.from_bytes(m_bytes, byteorder='big')
    return m_int


def generate_seed(name, age):
    age = int(age)
    name_encoded = encode(name)
    seed = name_encoded*10 ^ (len(str(name_encoded))) + age
    seed = seed % (2^32-1)
    if seed < 1000:
        seed *= 1000

    return seed


def output_image(mode, seed):
    with st.spinner("Consulting our local Panditji..."):
        generate_images(network_pkl=pkl_dict[mode],
                        seeds=[seed],
                        truncation_psi=1,
                        outdir='{0}_temp'.format(mode))

    image = Image.open('{0}_temp/seed{1}.png'.format(mode, seed))
    st.image(image, mode)


def main():
    st.header("If I was _, what would I look like? 🤔")

    name = st.text_input("What is your name?", "Name")
    age = st.number_input("What is your age?", 0)

    seed = generate_seed(name, age)

    cols = st.columns(4)

    b1 = cols[0].button("Someone else 🧑")
    if b1:
        output_image("Human", seed)

    b2 = cols[1].button("A Painting 🎨")
    if b2:
        output_image("Painting", seed)

    b3 = cols[2].button("An Animal 🧸")
    if b3:
        output_image("Animal", seed)

    b4 = cols[3].button("All!")
    if b4:
        output_image("Human", seed)
        output_image("Painting", seed)
        output_image("Animal", seed)


if __name__ == "__main__":
    main()
