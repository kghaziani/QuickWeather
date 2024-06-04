document.getElementById('search-button').addEventListener('click', function() {
    const ingredient = document.getElementById('ingredient-input').value;
    if (ingredient === '') return;

    fetch(`https://www.themealdb.com/api/json/v1/1/filter.php?i=${ingredient}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            const recipes = data.meals;
            const recipesContainer = document.getElementById('recipes');
            recipesContainer.innerHTML = '';

            if (recipes) {
                recipes.forEach(recipe => {
                    const recipeCard = `
                        <div class="col-md-4">
                            <div class="card">
                                <img src="${recipe.strMealThumb}" class="card-img-top" alt="${recipe.strMeal}">
                                <div class="card-body">
                                    <h5 class="card-title">${recipe.strMeal}</h5>
                                    <button class="btn btn-primary" onclick="getRecipeDetails(${recipe.idMeal})">View Recipe</button>
                                </div>
                            </div>
                        </div>
                    `;
                    recipesContainer.insertAdjacentHTML('beforeend', recipeCard);
                });
            } else {
                recipesContainer.innerHTML = '<p>No recipes found.</p>';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            const recipesContainer = document.getElementById('recipes');
            recipesContainer.innerHTML = '<p>Error fetching recipes. Please try again later.</p>';
        });
});

function getRecipeDetails(id) {
    fetch(`https://www.themealdb.com/api/json/v1/1/lookup.php?i=${id}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            const recipe = data.meals[0];
            const recipeDetails = `
                <div class="modal fade" id="recipeModal" tabindex="-1" aria-labelledby="recipeModalLabel" aria-hidden="true">
                    <div class="modal-dialog modal-lg">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="recipeModalLabel">${recipe.strMeal}</h5>
                                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                    <span aria-hidden="true">&times;</span>
                                </button>
                            </div>
                            <div class="modal-body">
                                <img src="${recipe.strMealThumb}" class="img-fluid mb-3" alt="${recipe.strMeal}">
                                <h5>Ingredients</h5>
                                <ul>
                                    ${Object.keys(recipe)
                                        .filter(key => key.startsWith('strIngredient') && recipe[key])
                                        .map(key => `<li>${recipe[key]} - ${recipe['strMeasure' + key.slice(13)]}</li>`)
                                        .join('')}
                                </ul>
                                <h5>Instructions</h5>
                                <p>${recipe.strInstructions}</p>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            document.body.insertAdjacentHTML('beforeend', recipeDetails);
            $('#recipeModal').modal('show');
            $('#recipeModal').on('hidden.bs.modal', function () {
                $(this).remove();
            });
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error fetching recipe details. Please try again later.');
        });
}
