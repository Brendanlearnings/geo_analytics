import pandas as pd
import pydeck as pdk

# DATA_URL = "https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/bart-lines.json"
# df = pd.read_json(DATA_URL)

# url = "https://raw.githubusercontent.com/Brendanlearnings/geo_analytics/main/test.json"


# df2 = pd.read_json(url)

# df.to_csv('original.csv')
# df2.to_csv('mine.csv')
df = pd.read_csv('mine.csv')

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


df["color"] = df["color"].apply(hex_to_rgb)

print(df.head(10))
view_state = pdk.ViewState(latitude=37.782556, longitude=-122.3484867, zoom=10)

layer = pdk.Layer(
    type="PathLayer",
    data=df,
    pickable=True,
    get_color="color",
    width_scale=20,
    width_min_pixels=2,
    get_path="path",
    get_width=5,
)


r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{name}"})
r.to_html("mine_path_layer.html")