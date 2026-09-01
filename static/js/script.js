const input_search = document.querySelector('input[name="q"]');

input_search.addEventListener('input', async () => {
    const value = input_search.value.trim();
    const response = await fetch(`/store/search?q=${value}`,
        {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        }
    );
    const data = await response.json();
    showSearchResults(data);
});


const showSearchResults = ({ products }) => {
    if (document.querySelector('.suggestion-block')) {
        document.querySelector('.suggestion-block').remove();
    }

    if (products.length > 0) {
      const suggestionBlock = document.createElement('div');
      suggestionBlock.className = 'suggestion-block';

      products.forEach(product => {
          const productBlock = document.createElement('a');
          productBlock.className = 'suggestion-item';
          productBlock.href = `/store/${product.id}`;
          productBlock.textContent = product.name;

          suggestionBlock.appendChild(productBlock);
    })

    input_search.after(suggestionBlock);
    }
}


document.body.addEventListener('click', (e) => {
    if (!e.target.classList.contains('suggestion-block')) {
        document.querySelector('.suggestion-block').remove();
    }
})