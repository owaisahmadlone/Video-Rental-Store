var updateBtns = document.getElementsByClassName('update-cart')

for(var i=0;i<updateBtns.length;i++){
    updateBtns[i].addEventListener('click',function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:',productId,'action:', action)
        console.log('USER: ', user)
        if(user === "AnonymousUser"){
            console.log('Not logged in')}else{
                UpdateuserOrder(productId,action)
            }
    })
}

function UpdateuserOrder(productId,action){
    console.log('user is logged in, sending data...')

    const url = '/update_item/';

    fetch(url, {
        method:'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId': productId, 'action': action})
    })

    .then((response) => {
		   return response.json();
		})
		.then((data) => {
		    console.log('data:', data)
            location.reload()
		});
}

//Function for searchBar and search Button
document.getElementById('search-button').addEventListener('click', function(event) {
    event.preventDefault(); // prevent default form submission behavior
    const term = document.getElementById('search-bar').value.toLowerCase();
    fetch('/get-products/')
        .then(response => response.json())
        .then(data => {
            const products = data.products;
            let matchingProducts=undefined;
            if(term.length ===  1){
                 matchingProducts = products.filter(product => {
                      return product.name.toLowerCase().startsWith(term.toLowerCase());
                    });

            }
            if(term.length > 1) {
                 matchingProducts = products.filter(product => {
                     return (product.name.toLowerCase().includes(term.toLowerCase()) || product.genre.toLowerCase().includes(term.toLowerCase()));
                 });
            }
            const allDivs = document.querySelectorAll('.col-lg-4');
            allDivs.forEach(div => {
                const productName = div.id;
                console.log(productName);
                if(matchingProducts.some(p => (p.name === productName))){
                    div.classList.remove('hidden');
                } else {
                    div.classList.add('hidden');
                }
            });

        });
});