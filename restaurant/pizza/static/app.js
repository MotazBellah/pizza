var menu = document.getElementById('menu')
var total = 0;
var topping = [];
var items = '';

// $(document).on('submit', '.add-to-carts', function(e) {
//     e.preventDefault();
//
//     $.ajax({
//         type: 'post',
//         url: '/addFood',
//         data: {
//             food: $('.food').val(),
//             add1: $('.small').val(),
//             add2: $('.larg').val(),
//             topping1: $('.topping').val(),
//             csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
//         },
//         success: function () {
//             alert('Added to your carts')
//         }
//     });
// });



menu.addEventListener('click', (e) => {
    // selectionLimit(2, 'test');
    selectionLimit(2, 'tw');
    selectionLimit(3, 'th');
    selectionLimit(2, 'two-item');
    selectionLimit(3, 'three-item');

    if (e.target.tagName === 'INPUT') {
        var form = e.target.parentNode.parentNode.id;
        var price = e.target.value
        var food = e.target.parentNode.parentNode.childNodes[3].value
        console.log(e.target.parentNode.parentNode.childNodes);
        const select1 = e.target.parentNode.parentNode.childNodes[5]
        // const values = Array.from(selectedd).map(el => el.value);
        // const selectedValues = values.filter((x) => x.selected).map((x)=>x.value);
        var selected1 = []
        for (var i = 0; i < select1.length; i++) {
        if (select1.options[i].selected) {
            selected1.push(select1.options[i].value);
        }
    }

        console.log(selected1);
        console.log(price);
        console.log(food);
        var check = true
        var id = "#" + form
        // console.log($(id+'.food').val());

        console.log("#" + form);
        $(document).on('submit', id, function(e) {
            e.preventDefault();
            if (check) {
                $.ajax({
                    type: 'post',
                    url: '/addFood',
                    data: {
                        // food: $('.food').val(),
                        // add1: $('.small').val(),
                        // add2: $('.larg').val(),
                        // topping1: $('.topping').val(),
                        // csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                        food: food,
                        add2: price,
                        topping1: selected1.toString(),
                        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                    },
                    success: function () {
                        alert('Added to your carts')

                    }

                });
                check = false;

            }


        });

    }

    // console.log(e.target.parentNode);
    // console.log(e.target.value);
    if (e.target.tagName === 'INPUT') {
        var adds = ['1 topping', '2 toppings', '3 toppings', '1 item', '2 items', '3 items']
        if (e.target.checked) {

            e.target.parentElement.firstChild.nextSibling.checked = true;
            // console.log(e.target.parentElement.firstChild.nextSibling.value);
            var top = e.target.parentElement.firstChild.nextSibling.value
            if (adds.includes(top)) {
                // console.log(top);
                if (top === '1 topping') {
                    document.getElementsByClassName("one")[0].style.display = 'block';
                }
                if (top === '2 toppings') {
                    document.getElementsByClassName("two")[0].style.display = 'block';
                    selectionLimit(2, 'tw');
                }
                if (top === '3 toppings') {
                    document.getElementsByClassName("three")[0].style.display = 'block';
                    selectionLimit(3, 'th');
                }
                if (top === '1 item') {
                    document.getElementsByClassName("item1")[0].style.display = 'block';

                }
                if (top === '2 items') {
                    document.getElementsByClassName("item2")[0].style.display = 'block';
                    selectionLimit(2, 'two-item');
                }
                if (top === '3 items') {
                    document.getElementsByClassName("item3")[0].style.display = 'block';
                    selectionLimit(3, 'three-item');
                }
            }
            total += parseFloat(e.target.value);
        } else {

            total -= parseFloat(e.target.value);
            e.target.parentElement.firstChild.nextSibling.checked = false;
            var top = e.target.parentElement.firstChild.nextSibling.value
            if (adds.includes(top)) {
                if (top === '1 topping') {
                    document.getElementsByClassName("one")[0].style.display = 'none';
                }
                if (top === '2 toppings') {
                    document.getElementsByClassName("two")[0].style.display = 'none';

                }
                if (top === '3 toppings') {
                    document.getElementsByClassName("three")[0].style.display = 'none';

                }
                if (top === '1 item') {
                    document.getElementsByClassName("item1")[0].style.display = 'none';

                }
                if (top === '2 items') {
                    document.getElementsByClassName("item2")[0].style.display = 'none';

                }
                if (top === '3 items') {
                    document.getElementsByClassName("item3")[0].style.display = 'none';

                }
            }

        }
        if (total < 0) {
            total = 0
        }
    }
    // console.log(items);
    // var p = document.createElement('p');
    // if (e.target.tagName === 'SELECT') {
    //     var toppingArea = document.getElementById('selected-toopings');
    //     if (e.target.value !== 'Select') {
    //         if (!topping.includes(e.target.value)) {
    //             p.textContent = e.target.value;
    //             p.className = 'food';
    //             toppingArea.appendChild(p);
    //             topping.push(e.target.value)
    //         }
    //     }
    // }
    //
    // if (e.target.tagName === 'P' && e.target.className === 'food') {
    //     var el = e.target;
    //     var index = topping.indexOf(e.target.value);
    //     el.parentNode.removeChild(el);
    //     topping.splice(index, 1);
    // }

    // console.log(total);
    // console.log(topping);

});

function selectionLimit(limit, id) {
    document.getElementById(id).addEventListener("change", function() {
        // console.log(e.target.value);
        if ($(this).val().length > limit) {
            $(this).val(null);
            alert('You can select upto ' + limit.toString() +' options only');
        }
    });
}
