document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('record-form');
    const typeSelect = document.getElementById('id_type');
    const categorySelect = document.getElementById('id_category');
    const subcategorySelect = document.getElementById('id_subcategory');

    const initialType = typeSelect.value;
    const initialCategory = form.dataset.initialCategory || "";
    const initialSubcat = form.dataset.initialSubcat || "";
    const successUrl = form.dataset.successUrl;
    console.log(form.dataset)
    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }

    function loadCategories(typeSlug, selectedCatSlug=null) {
        categorySelect.innerHTML = '<option value="">---------</option>';
        subcategorySelect.innerHTML = '<option value="">---------</option>';

        if (!typeSlug) return;

        fetch(`${window.location.pathname}?type=${typeSlug}`, { headers: {'X-CAT-AJAX': 'true'} })
            .then(resp => resp.json())
            .then(data => {
                const categories = JSON.parse(data.categories);
                categories.forEach(cat => {
                    const option = document.createElement('option');
                    option.value = cat.fields.slug;
                    option.textContent = cat.fields.name;
                    categorySelect.appendChild(option);
                });

                if (selectedCatSlug) loadSubcategories(selectedCatSlug, initialSubcat);
            })
            .catch(err => console.error('Ошибка загрузки категорий:', err));
    }

    function loadSubcategories(categorySlug, selectedSubSlug=null) {
        subcategorySelect.innerHTML = '<option value="">---------</option>';
        if (!categorySlug) return;

        fetch(`${window.location.pathname}?category=${categorySlug}`, { headers: {'X-SUBCAT-AJAX': 'true'} })
            .then(resp => resp.json())
            .then(data => {
                const subs = JSON.parse(data.subcategories);
                subs.forEach(sub => {
                    const option = document.createElement('option');
                    option.value = sub.fields.slug;
                    option.textContent = sub.fields.name;
                    subcategorySelect.appendChild(option);
                });
            })
            .catch(err => console.error('Ошибка загрузки подкатегорий:', err));
    }

    if (initialType) loadCategories(initialType, initialCategory);

    typeSelect.addEventListener('change', () => loadCategories(typeSelect.value));
    categorySelect.addEventListener('change', () => loadSubcategories(categorySelect.value));
    form.addEventListener('submit', function(event){
        event.preventDefault();

        const formData = new FormData(form);

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {'X-CSRFToken': getCSRFToken(), 'Accept': 'application/json'}
        })
        .then(resp => {
            if (resp.status === 200) {
                window.location.href = successUrl;
            }
        })

        .catch(err => console.error('Ошибка при отправке формы:', err));
    });
});
