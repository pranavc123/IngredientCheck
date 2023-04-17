from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

allergens = ["parabens", "sulfates", "fragrance", "formaldehyde", "phthalates"]

def check_for_allergens(ingredient_list):
    found_allergens = []
    for allergen in allergens:
        if allergen in ingredient_list:
            found_allergens.append(allergen)
    return found_allergens

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product_name = request.form['product_name']
        return redirect(url_for('result', product_name=product_name))
    return render_template('index.html')

@app.route('/result/<product_name>')
def result(product_name):
    # Make API request
    url = f"https://world.openbeautyfacts.org/cgi/search.pl?search_terms={product_name}&search_simple=1&action=process&json=1"
    response = requests.get(url)
    data = response.json()

    # Extract the first product's ingredients
    if data['count'] > 0:
        product = data['products'][0]
        ingredients = product['ingredients_text'].lower()
        ingredient_list = [ingredient.strip() for ingredient in ingredients.split(",")]

        # Check for allergens
        found_allergens = check_for_allergens(ingredient_list)

        return render_template('result.html', product=product, found_allergens=found_allergens)

    return "Product not found. Please try again."

if __name__ == '__main__':
    app.run(debug=True)
