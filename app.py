import streamlit as st
from PIL import Image

from config import settings
from color_service import ColourService
from ui_helper import CSS, colour_strip_html, swatch_card_html


@st.cache_resource
def get_service() -> ColourService:
    return ColourService()

def setup_page():
    st.set_page_config(
        page_title=f"{settings.app_title} — Colour Extractor",
        page_icon=settings.app_icon,
        layout=settings.app_layout,
    )

    st.markdown(CSS, unsafe_allow_html=True)


def render_header():
    st.title(f"{settings.app_icon} {settings.app_title}")
    st.caption(settings.app_caption)


def render_controls():
    n_colours = st.slider(
        "Number of colours to extract",
        min_value=settings.min_colours,
        max_value=settings.max_colours,
        value=settings.default_n_colours,
    )

    uploaded = st.file_uploader(
        "Drop an image here",
        type=settings.allowed_extensions,
    )

    return n_colours, uploaded


def render_results(uploaded: st.runtime.uploaded_file_manager.UploadedFile, n_colours: int):
    service = get_service()

    image: Image.Image = Image.open(uploaded)
    col_image, col_palette = st.columns(2)

    with col_image:
        st.image(
            image,
            caption=f"{uploaded.name}  ·  {image.width}×{image.height}px",
            use_container_width=True,
        )

    with st.spinner("Analysing colours with KMeans…"):
        colours = service.extract(image, n_colours)

    with col_palette:
        st.markdown("**Colour strip**")
        st.markdown(colour_strip_html(colours), unsafe_allow_html=True)

        st.markdown(f"**Top {n_colours} colours**")
        max_pct = colours[0].percentage  # list is sorted descending — first = most dominant
        for rank, colour in enumerate(colours, start=1):
            st.markdown(swatch_card_html(colour, rank, max_pct), unsafe_allow_html=True)

    st.download_button(
        label="⬇ Download palette (.txt)",
        data=service.to_palette_txt(colours),
        file_name=f"{uploaded.name.rsplit('.', 1)[0]}_palette.txt",
        mime="text/plain",
    )


def main():
    setup_page()
    render_header()

    n_colours, uploaded = render_controls()

    if not uploaded:
        st.stop()

    render_results(uploaded, n_colours)


if __name__ == "__main__":
    main()