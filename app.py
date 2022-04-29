import streamlit as st
from gen_images import generate_images
from PIL import Image
import datetime


pkl_dict = {"Animal": "https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan3/"
                      "versions/1/files/stylegan3-r-afhqv2-512x512.pkl",
            "Human": "https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan3/"
                     "versions/1/files/stylegan3-r-ffhq-1024x1024.pkl",
            "Painting": "https://api.ngc.nvidia.com/v2/models/nvidia/research/stylegan3/"
                        "versions/1/files/stylegan3-r-metfaces-1024x1024.pkl"}

st.set_page_config(page_title="Param",page_icon="Data/ParamSLogo.jpeg")


def footer():
    footer="""
            <style>
            .footer {
            left: 0;
            bottom: 0;
            width: 100%;
            color: black;
            text-align: center;
            }
            </style>
            <br/>
            <br/>
            <br/>
            <br/>
            <br/>
            <div class="footer">
            <p>Credits to the <a href="https://github.com/NVlabs/stylegan3">StyleGAN3 creators</a> <b> <a style='display: block; text-align: center;'">Param Innovation</a> </b></p>
            </div>
            """
    st.markdown(footer,unsafe_allow_html=True)


def encode_name(name):
    m_bytes = name.encode("utf-8")
    m_int = int.from_bytes(m_bytes, byteorder='big')
    return m_int


def encode_age(date):
    return date.year*10000 + date.month*100 + date.day


def generate_seed(name, date):
    age_encoded = encode_age(date)
    name_encoded = encode_name(name)
    seed = name_encoded + age_encoded
    seed = seed % (2 ^ 32 - 1)
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
    image = Image.open('Data/ParamHQLogo.png')
    st.image(image, width=200)
    st.header("If I was _, what would I look like? 🤔")

    name = st.text_input("What is your name?", "Name")
    date = st.date_input("When is your birthday?", datetime.date(2000, 1, 1))

    seed = generate_seed(name, date)

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

    footer()


if __name__ == "__main__":
    main()
