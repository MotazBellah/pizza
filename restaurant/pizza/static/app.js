var menu = document.getElementById('menu')
var total = 0;
var topping = [];
var items = '';


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
        var typeID = e.target.parentNode.parentNode.childNodes[3].id;
        console.log(e.target.parentNode.parentNode.childNodes);
        const select1 = e.target.parentNode.parentNode.childNodes[5]

        var selected1 = []
        if (select1) {
            for (var i = 0; i < select1.length; i++) {
            if (select1.options[i].selected) {
                selected1.push(select1.options[i].value);
            }
        }

        }
        console.log(typeID);
        console.log(selected1.length);
        console.log(price);
        console.log(food);
        var check = true
        var id = "#" + form

        console.log("#" + form);
        $(document).on('submit', id, function(e) {
            e.preventDefault();
            if (check) {
                if ((food=='2 toppings'||food=='2 items') && selected1.length < 2) {
                    alert("Please select 2 toppings")
                    check = false;
                    return
                }
                if ((food=='3 toppings'||food=='3 items') && selected1.length < 3) {
                    alert("Please select 3 toppings")
                    check = false;
                    return
                }
                $.ajax({
                    type: 'post',
                    url: '/addFood',
                    data: {
                        food: food,
                        add2: price,
                        topping1: selected1.toString(),
                        id: typeID,
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

});

function selectionLimit(limit, id) {
    var el = document.getElementById(id);
    if (el) {
        el.addEventListener("change", function() {
            // console.log(e.target.value);
            if ($(this).val().length > limit) {
                $(this).val(null);
                alert('You can select upto ' + limit.toString() +' options only');
            }
        });
    }

}
