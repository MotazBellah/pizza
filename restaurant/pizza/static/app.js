alert('h');

var menu = document.getElementById('menu')
var total = 0;
menu.addEventListener('click', (e) => {

    console.log(e.target.tagName);
    if (e.target.tagName === 'INPUT') {
        if (e.target.checked) {
            alert(e.target.value);
            total += parseFloat(e.target.value);
        } else {
            total -= parseFloat(e.target.value);
        }

    }
    console.log(total);
});
