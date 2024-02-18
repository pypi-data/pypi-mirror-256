import streamlit.components.v1 as components
import uuid
from pathlib import Path

def os_searchbutton(label="Search Octostar", key=None, help="Click to search octostar", concept=None, concepts=None):
    if key is None:
        key = str(uuid.uuid4())
    
    component_id = str(uuid.uuid4());
    defaultConcept = "false"
    if concept:
        defaultConcept = [concept]
    elif concepts:
        defaultConcept = concepts

    frontend_dir = (Path(__file__).parent / "frontend").absolute()
    component_js_path = frontend_dir / 'streamlit-component-lib.js'

    with open(component_js_path, 'r', encoding='utf-8') as file:
        component_js_ = file.read()
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Octostar Search Button</title>
        <script>
{component_js_}
        </script>

   <style>
   body {{
    margin: 0;
   }}
  .button {{   
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0.25rem 0.75rem;
            border-radius: 0.5rem;
            font-size: 1rem;
            font-family: "Source Sans Pro", sans-serif;
            font-weight: 400;
            color: rgb(49, 51, 63);
            background-color: rgb(255, 255, 255);
            border: 1px solid rgba(9, 30, 66, 0.2);
            cursor: pointer;
            user-select: none;
            text-transform: none;
            margin: 0px;
            width: auto;
            min-height: 38px;
            min-height: 38px;
            -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
            -webkit-font-smoothing: auto;
            color-scheme: light;
            box-sizing: border-box;
        }}
    </style>    </head>
    <body>
        <div class="div1">
            <button class='button' id="{component_id}" title="{help}">
                {label}
            </button>
        </div>

    <script>
        const component_id = "{component_id}";
        const options = {{}}
        if ({defaultConcept}) {{
            options['defaultConcept'] = {defaultConcept};
        }}

            const button = document.getElementById(component_id);
            const onClickTopic = "{key}";


            window.parent.octostar.on(onClickTopic, (data) => {{
                console.log("onClickTopic", data);
                  Streamlit.setComponentValue(data);
            }})
            button.addEventListener("click", ()=> window.parent.octostar.callReplyingTo(
                    'octostar:desktop:searchXperience', onClickTopic, 
                    {{...options}}));

    </script>
    </body>
    </html>
    """
    components.html(html, height=40)
