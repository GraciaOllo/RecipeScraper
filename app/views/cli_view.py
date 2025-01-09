def display_recipe(recipe):
    print(f"Title: {recipe['title']}")
    print("\nIngredients:")
    for ingredient in recipe['ingredients']:
        print(f"- {ingredient}")
    print("\nInstructions:")
    for i, step in enumerate(recipe['instructions'], 1):
        print(f"{i}. {step}")
