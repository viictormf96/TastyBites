// Mantenemos el nombre de la función original para la paginación
function changePage(pageNumber) {
  const url = new URL(window.location.href);
  url.searchParams.set("page", pageNumber);
  window.location.href = url.toString();
}

/**
 * Función genérica para actualizar parámetros en la URL.
 * Mantiene la lógica de resetear a página 1 al filtrar.
 */
const updateRecipeParam = (key, value) => {
  const url = new URL(window.location.href);

  if (value) {
    url.searchParams.set(key, value);
  } else {
    url.searchParams.delete(key);
  }

  // Si estamos filtrando o cambiando vista, volvemos a la página 1
  if (url.searchParams.has("page")) {
    url.searchParams.set("page", "1");
  }

  window.location.href = url.toString();
};

const initRecipeFilters = () => {
  // 1. Buscamos los elementos por sus IDs originales
  const timeSortSelect = document.getElementById("time-sort");
  const difficultySort = document.getElementById("difficulty-sort");
  const caloriesSort = document.getElementById("calories-sort");
  const dietSort = document.getElementById("diet-sort");
  const selectSort = document.getElementById("sort-recipes");

  const urlParams = new URLSearchParams(window.location.search);

  // 2. Mapeo de configuración: ID del elemento -> Nombre del parámetro en URL
  const filters = [
    { el: timeSortSelect, param: "time" },
    { el: difficultySort, param: "difficulty" },
    { el: caloriesSort, param: "calories" },
    { el: dietSort, param: "diet" },
    { el: selectSort, param: "sort" }
  ];

  filters.forEach(({ el, param }) => {
    if (!el) return;

    // Sincronizar el estado del select con la URL actual al cargar
    const currentVal = urlParams.get(param);
    if (currentVal) {
      el.value = currentVal;
    }

    // Escuchar el evento de cambio de forma genérica
    el.addEventListener("change", function() {
      updateRecipeParam(param, this.value);
    });
  });

  // 3. Manejo de vistas (Grid / List)
  const ViewList = document.getElementById("view-list");
  const ViewGrid = document.getElementById("view-grid");

  if (ViewGrid) {
    ViewGrid.addEventListener("click", (e) => {
      e.preventDefault();
      updateRecipeParam("view", "grid");
    });
  }

  if (ViewList) {
    ViewList.addEventListener("click", (e) => {
      e.preventDefault();
      updateRecipeParam("view", "list");
    });
  }
};

// Ejecución segura del inicializador
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initRecipeFilters);
} else {
  initRecipeFilters();
}