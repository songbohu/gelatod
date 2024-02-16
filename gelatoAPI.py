from PIL import Image, ImageDraw
import difflib

flavor_colors = {
    'Baked Vanilla': '#F3E5AB',
    'Manuka Honey & Fig': '#D2B48C',
    'Roasted Banana': '#FFE135',
    'Caramel': '#A67B5B',
    'King’s College Lavender': '#E6E6FA',
    'Gianduja (vegan)': '#6B4423',
    'Passion Fruit Sorbet (vegan)': '#FFD700',
    'House Yoghurt': '#FFFFF0',
    'Dark Chocolate & Sea Salt (vegan)': '#8B4513',
    'Treacle Cake': '#664229',
    'Strawberries & Cream': '#FFC0CB',
    'Coconut, Raspberry Ripple (vegan)': '#FF3366',
    'Organic Whisky; Nc’nean': '#DAA520',
    'coconut and ube': '#7D26CD'
}


def draw_ice_cream(flavours, size, container):

    width, height = 400, 500
    img = Image.new('RGB', (width, height), 'lightblue')
    draw = ImageDraw.Draw(img)

    sizes = {'Single Scoop': 1, 'Double Scoop': 2, 'Triple Scoop': 3}
    num_scoops = sizes[size]

    if container == 'Paper Cup':
        container_adjust_y = 50
    else:
        container_adjust_y = 20


    scoop_y = 300 + container_adjust_y- (100 * num_scoops)
    for i in range(num_scoops):
        flavor_color = flavor_colors.get(flavours[i], 'lightblue')  # Default to white if flavor not found
        draw.ellipse([150, scoop_y, 250, scoop_y + 100], fill=flavor_color)
        scoop_y += 100  # Move up for next scoop

    if container == 'Normal Cone':
        draw.polygon([(160, 300), (240, 300), (200, 400)], fill='#D2B48C')  # Cone
    elif container == 'Paper Cup':
        draw.rectangle([150, 300, 250, 400], fill='#F5F5F5')  # Cup
    elif container == 'Chocolate Dipped Waffle Cone':
        draw.polygon([(160, 300), (240, 300), (200, 400)], fill='#8B4513')  # Chocolate Cone

    # Save image
    img_path = './ice_cream.png'
    img.save(img_path)
    return img_path


def find_most_similar(available_values, input_values):
    matches = []
    for input_value in input_values:
        best_match = difflib.get_close_matches(input_value, available_values, n=1, cutoff=0.0)
        matched_value = best_match[0] if best_match else None
        matches.append(matched_value)

    return matches


def get_gelato(state):


    flavours = state["flavours"]
    size = state["size"]
    container = state["container"]

    flavours = find_most_similar(flavor_colors.keys(), flavours)

    size = find_most_similar(["Single Scoop", "Double Scoop", "Triple Scoop"], [size])[0]
    container = find_most_similar(["Normal Cone", "Paper Cup", "Chocolate Dipped Waffle Cone" ], [container])[0]
    sizes = {'Single Scoop': 1, 'Double Scoop': 2, 'Triple Scoop': 3}
    num_scoops = sizes[size]

    if len(flavours) < num_scoops:
        num_scoops = len(flavours)
        size = ["Single Scoop", "Double Scoop", "Triple Scoop"][num_scoops-1]
    else:
        flavours = flavours[-num_scoops:]
    return draw_ice_cream(flavours, size, container)


if __name__ == '__main__':

    state = {
    "flavours": ["House Yoghurt", "ube"],
    "size": 'Double Scoops',
    "container": "cone",
    }

    image_path = get_gelato(state)
    print(f"Image saved to {image_path}")