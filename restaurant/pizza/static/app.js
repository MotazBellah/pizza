var menu = document.getElementById('menu')
var total = 0;
var topping = []
menu.addEventListener('click', (e) => {

    console.log(e.target.tagName);
    console.log(e.target.value);
    if (e.target.tagName === 'INPUT') {
        if (e.target.checked) {
            // alert(e.target.value);
            total += parseFloat(e.target.value);
        } else {
            total -= parseFloat(e.target.value);
        }
        if (total < 0) {
            total = 0
        }
    }

    var p = document.createElement('p');
    if (e.target.tagName === 'SELECT') {
        var toppingArea = document.getElementById('selected-toopings');
        if (e.target.value !== 'Select') {
            if (!topping.includes(e.target.value)) {
                p.textContent = e.target.value;
                p.className = 'food';
                toppingArea.appendChild(p);
                topping.push(e.target.value)
            }
        }
    }

    if (e.target.tagName === 'P' && e.target.className === 'food') {
        var el = e.target;
        var index = topping.indexOf(e.target.value);
        el.parentNode.removeChild(el);
        topping.splice(index, 1);
    }

    console.log(total);
    console.log(topping);

});
