function changePage(pageNumber) {
  const url = new URL(window.location.href);

  url.searchParams.set("page", pageNumber);

  window.location.href = url.toString();
}

const initRecipeFilters = () => {
    // 1. Buscamos el select por ID. Asegúrate de que en recipes_filter.html 
    const timeSortSelect = document.getElementById("time-sort");
    const difficultySort = document.getElementById("difficulty-sort");
    const caloriesSort = document.getElementById("calories-sort");
    const dietSort = document.getElementById("diet-sort");

    // 2. Sincronizar el estado del select con la URL actual al cargar la página
    const urlParams = new URLSearchParams(window.location.search);
    const currentTimeParam = urlParams.get("time");
    const currentDifficultyParam = urlParams.get("difficulty");
    const currentCaloriesParam = urlParams.get("calories");
    const currentDietParam = urlParams.get("diet");

    if (currentTimeParam) {
      timeSortSelect.value = currentTimeParam;
    }

    if (currentDifficultyParam) {
      difficultySort.value = currentDifficultyParam;
    }

    if (currentCaloriesParam) {
      caloriesSort.value = currentCaloriesParam;
    }

    if (currentDietParam) {
      dietSort.value = currentDietParam;
    }

    // 3. Escuchar el evento de cambio
    timeSortSelect.addEventListener("change", function() {
        const selectedValue = this.value;
        const url = new URL(window.location.href);

        // Si hay un valor seleccionado, lo ponemos en la URL. 
        // Si es vacío (la opción por defecto), lo eliminamos.
        if (selectedValue) {
            url.searchParams.set("time", selectedValue);
        } else {
            url.searchParams.delete("time");
        }

        // Importante: Si filtras, debes volver a la página 1 para evitar errores 404
        if (url.searchParams.has("page")) {
            url.searchParams.set("page", "1");
        }

        // Redireccionar a la nueva URL
        window.location.href = url.toString();
    });

    difficultySort.addEventListener("change", function() {
        const selectedValue = this.value;
        const url = new URL(window.location.href);

        // Si hay un valor seleccionado, lo ponemos en la URL. 
        // Si es vacío (la opción por defecto), lo eliminamos.
        if (selectedValue) {
            url.searchParams.set("difficulty", selectedValue);
        } else {
            url.searchParams.delete("difficulty");
        }

        // Importante: Si filtras, debes volver a la página 1 para evitar errores 404
        if (url.searchParams.has("page")) {
            url.searchParams.set("page", "1");
        }

        // Redireccionar a la nueva URL
        window.location.href = url.toString();
    });

    caloriesSort.addEventListener("change", function() {
        const selectedValue = this.value;
        const url = new URL(window.location.href);

        // Si hay un valor seleccionado, lo ponemos en la URL. 
        // Si es vacío (la opción por defecto), lo eliminamos.
        if (selectedValue) {
            url.searchParams.set("calories", selectedValue);
        } else {
            url.searchParams.delete("calories");
        }

        // Importante: Si filtras, debes volver a la página 1 para evitar errores 404
        if (url.searchParams.has("page")) {
            url.searchParams.set("page", "1");
        }

        // Redireccionar a la nueva URL
        window.location.href = url.toString();
    });

    dietSort.addEventListener("change", function() {
        const selectedValue = this.value;
        const url = new URL(window.location.href);

        // Si hay un valor seleccionado, lo ponemos en la URL. 
        // Si es vacío (la opción por defecto), lo eliminamos.
        if (selectedValue) {
            url.searchParams.set("diet", selectedValue);
        } else {
            url.searchParams.delete("diet");
        }

        // Importante: Si filtras, debes volver a la página 1 para evitar errores 404
        if (url.searchParams.has("page")) {
            url.searchParams.set("page", "1");
        }

        // Redireccionar a la nueva URL
        window.location.href = url.toString();
    });
};

// Ejecutamos la función cuando el DOM esté listo
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initRecipeFilters);
} else {
    initRecipeFilters();
}

document.addEventListener("DOMContentLoaded", () => {
  const select = document.getElementById("sort-recipes");

  // 1. Detectar el cambio en el select
  select.addEventListener("change", function () {
    const value = this.value;

    // 2. Obtener la URL actual y manipular los parámetros
    const url = new URL(window.location.href);

    // Seteamos el parámetro 'sort' con el valor del select
    url.searchParams.set("sort", value);

    // 3. Redirigir a la nueva URL (Esto dispara la vista en Django)
    window.location.href = url.toString();
  });

  const ViewList = document.getElementById("view-list");
  const ViewGrid = document.getElementById("view-grid");

  const updateViewParam = (viewMode, param) => {
    const url = new URL(window.location.href);
    
    url.searchParams.set(param, viewMode);

    if (param == "view"){
      url.searchParams.delete("page");
    }

    // Redirigir para que Django procese la nueva vista
    window.location.href = url.toString();
  };

  if (ViewGrid) {
    ViewGrid.addEventListener("click", (e) => {
      e.preventDefault();
      updateViewParam("grid", "view");
    });
  }

  if (ViewList) {
    ViewList.addEventListener("click", (e) => {
      e.preventDefault();
      updateViewParam("list", "view");
    });
  }


  // 4. Mantener la opción seleccionada después de que la página recargue
  const currentParams = new URLSearchParams(window.location.search);

  const activeSort = currentParams.get("sort");

  if (activeSort) {
    select.value = activeSort;
  }
});
