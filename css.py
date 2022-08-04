import plotly.io as pio

class CSS():

    # ///////////////////////////////////////////
    # ///                 main                ///
    # ///////////////////////////////////////////
    color_scheme = {
        "sidebar_background": "#FFFFFF",
        "sidebar_border": "#43bfe5",
        "main_background": "#EDFDFF",   # I like this color!
        "explanation_background": "#43bfe5",
        "explanation_text": "#F5F5F5",
        "horizontal_line": "#000000",
        "presets": "#E56943",
    }


    sidebar_width = ["16rem", "1rem"]

    sidebar_style = {
        "position": "fixed",
        "top": 0,
        # "left": 0,
        "right": 0,
        "bottom": 0,
        "width": sidebar_width[0],
        "background-color": color_scheme["sidebar_background"],
        "border-style": "solid",
        # "border-width": "8px 8px 0px 8px", # remove the bottom border # top, right, bottom, left
        "border-width": "8px 8px 8px 8px",
        "border-color": color_scheme["sidebar_border"],
        "padding-left": "10px",
        "padding-right": "10px",
        "padding-bottom": "10px",
    }

    outer_layout_style = {
        'margin-right': sidebar_width[0],
        'padding-right': "10px",
        "background-color": color_scheme["main_background"],
    }

    titlebar_style = {
        'margin-left': '10px',
        'padding-left': '10px',
        'padding-top': '10px',
        'top': '20px'
    }

    glossary_style = {"margin-top": "10px"}



    # ///////////////////////////////////////////
    # ///            graph frame              ///
    # ///////////////////////////////////////////

        # define HTML styles for text and dropdown menus. Use this to change font size, alignment, etc.
    text_style = {
        # "display": "inline-block", # if you take this out, all successive elements will be displayed on separate lines
        # "display": "flex",
        "display": "inline-block",
        # "transform": "translateY(0%)", # vertical alignment
        # "position": "relative",
        "margin-left": "10px", # adds a horizontal space between dropdowns menus and next chunk of text
        "margin-right": "10px", # adds a horizontal space between dropdowns menus and next chunk of text
        "font-size" : "18px",
        "font-family": "Arial",
        "padding-right": "15px",
        "line-height": "2", # line spacing
    }

    text_style_explanation = {
        "display": "inline-block",
        # "transform": "translateY(0%)", # vertical alignment
        # "position": "relative",

        # 'margin' affects the size of the bounding box
        "margin-left": "7px", # adds a horizontal space between dropdowns menus and next chunk of text
        "margin-right": "40px", # adds a horizontal space between dropdowns menus and next chunk of text
        "margin-top": "20px",
        "margin-bottom": "20px",
        "border-radius": "5px", # rounded corners!

        # 'padding' affects the positioning of the text withing the bounding box
        "padding-left": "30px",
        "padding-right": "30px",
        "padding-top": "0px",
        "padding-bottom": "0px",

        # font size and color
        "font-size" : "16px",
        "font-family": "Arial",
        "color": color_scheme["explanation_text"],
        "background-color": color_scheme["explanation_background"],

        "line-height": "1.6", # line spacing
    }

    filter_picker_style = text_style | {"display": "inline"}

    # text_style_bold = text_style_explanation |

    dropdown_style = {
        "display": "inline-block",
        "width": "50%",
        "height": "32px",
        "margin-left": "8px",
        "margin-right": "8px",
        "font-size": "16px",
        "font-family": "Arial",
        "vertical-align": "middle",
        # "line-height": "0%", # helps reduce the line spacing
    }

    dropdown_style_2 = dropdown_style | {
        "width": "300px",
        # "margin-right": "10px",
        # "margin-left": "10px",
        "overflow-y": "visible",
        "max-height": "100%",
    }

    dropdown_style_header = dropdown_style_2 | {
        "font-size": "20px",
        "font-weight": "bold",
        }

    date_picker_style = dropdown_style | {
        "display": "inline-block",
        "width": "290px",
        "height": "80%",
        "line-height": "150%",
    }




