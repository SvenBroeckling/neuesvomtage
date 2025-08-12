$(function () {
    // Modals
    $('#feedModal').on('show.bs.modal', function (event) {
        const trigger = $(event.relatedTarget);
        const modal = $(this);

        modal.find('h5').text(trigger.data('modal-title'));
        modal.find('.modal-body').load(trigger.data('update-url'));
    });

    $('#sortModal').on('hide.bs.modal', function (event) {
        location.reload();
    });

    // Sorting
    jQuery.fn.sortElements = function sortElements(selector = "div") {
        $("> " + selector, this[0]).sort(dec_sort).appendTo(this[0]);

        function dec_sort(a, b) {
            return ($(b).data("order")) < ($(a).data("order")) ? 1 : -1;
        }
    };

    function saveSortOrder() {
        let order = [];
        let hidden = [];
        $('.sortable li').each(function (idx, e) {
            order.push($(e).data('source-id'));
            if ($(e).data('sort-hidden')) {
                hidden.push($(e).data('source-id'));
            }
        });
        localStorage.setItem('sort-order', JSON.stringify(order));
        localStorage.setItem('sort-hidden', JSON.stringify(hidden));
    }

    function swapElements(elem1, elem2) {
        let t_elem1 = $(elem1).clone();
        let t_elem2 = $(elem2).clone();
        $(elem1).replaceWith(t_elem2);
        $(elem2).replaceWith(t_elem1);
    }

    let sort_sources = $('.sort-sources');
    sort_sources.on('click', '.sort-move-top', function (e) {
        let elem = $(this).parent();
        let container = $(this).parent().parent();
        container.prepend(elem);
        saveSortOrder();
    });

    sort_sources.on('click', '.sort-move-up', function (e) {
        swapElements($(this).parent(), $(this).parent().prev());
        saveSortOrder();
    });

    sort_sources.on('click', '.sort-move-down', function (e) {
        swapElements($(this).parent(), $(this).parent().next());
        saveSortOrder();
    });

    sort_sources.on('click', '.sort-hide', function (e) {
        if ($(this).parent().data('sort-hidden')) {
            $(this).parent().data('sort-hidden', null);
            $(this).parent().removeClass('list-group-item-danger')
        } else {
            $(this).parent().data('sort-hidden', true);
            $(this).parent().addClass('list-group-item-danger')
        }
        saveSortOrder();
    });

    $('.sortable').sortable({
        tolerance: 'pointer', items: 'li', placeholder: '<li class="list-group-item"></li>'
    }).bind('sortstart', function (e, ui) {
    }).bind('sortstop', function (e, ui) {
    }).bind('sortupdate', function (e, ui) {
        saveSortOrder();
    });

    // restore the hidden sources from localStorage
    var sort_hidden = localStorage.getItem('sort-hidden');
    if (sort_hidden != null) {
        var hidden = JSON.parse(sort_hidden);
        for (var i = 0; i < hidden.length; i++) {
            $('div.source[data-source-id="' + hidden[i] + '"]').hide();
            $('li.sort-source[data-source-id="' + hidden[i] + '"]').addClass('list-group-item-danger');
            $('li.sort-source[data-source-id="' + hidden[i] + '"]').data('sort-hidden', true);
        }
    }

    // restore the sort order from localStorage
    var sort_order = localStorage.getItem('sort-order');
    if (sort_order != null) {
        var order = JSON.parse(sort_order);
        for (var i = 0; i < order.length; i++) {
            $('div.source[data-source-id="' + order[i] + '"]').data('order', i);
            $('li.sort-source[data-source-id="' + order[i] + '"]').data('order', i);
        }
        $('div.sources').sortElements();
        $('ul.sort-sources').sortElements('li');
    }

    $('.top-10-show-all').on('click', function (e) {
        $(this).addClass('d-none');
        $('.top-10-rest').removeClass('d-none');
        e.preventDefault();
        return false;
    })

    var isMulti = document.body.classList.contains('layout-multi') || document.documentElement.classList.contains('layout-multi');
    if (isMulti) {
        $('.sources').masonry();
    }
});
