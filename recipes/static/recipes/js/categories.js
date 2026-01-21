const btnGrid = document.getElementById('btn-grid');
const btnList = document.getElementById('btn-list');
const container = document.getElementById('recipe-container');
btnGrid.addEventListener('click', () => {
    container.classList.remove('list-view');
    btnGrid.classList.add('active-view-btn');
    btnList.classList.remove('active-view-btn');
});
btnList.addEventListener('click', () => {
    container.classList.add('list-view');
    btnList.classList.add('active-view-btn');
    btnGrid.classList.remove('active-view-btn');
});