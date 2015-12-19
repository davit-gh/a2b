/* 

App Landing Template

http://www.templatemo.com/tm-474-app-landing

*/
function sourcefilter(val){
    var jo = $("#fbody").find("tr");
    
    //hide all the rows
    jo.hide();
    jo.filter(function (i, v) {
        var $t = $(this);
        if ($t[0].cells[0].innerText.trim() == val.value) {
            return true;
        }
        
        return false;
    })
    //show the rows that match.
    .show();
}
function destfilter(val){
    var jo = $("#fbody").find("tr");
    
    //hide all the rows
    jo.hide();
    jo.filter(function (i, v) {
        var $t = $(this);
        if ($t[0].cells[1].innerText.trim() == val.value) {
            return true;
        }
        
        return false;
    })
    //show the rows that match.
    .show();
}
jQuery(document).ready(function(){
    // jQuery.templatemo_is_chrome
    $.templatemo_is_chrome = /chrom(e|ium)/.test(navigator.userAgent.toLowerCase());
    // Template Mo menu hide
    $('table').each(function() {
        var currentPage = 0;
        var numPerPage = 3;
        var $table = $(this);
        $table.bind('repaginate', function() {
            $table.find('tbody tr').hide().slice(currentPage * numPerPage, (currentPage + 1) * numPerPage).show();
        });
        $table.trigger('repaginate');
        var numRows = $table.find('tbody tr').length;
        var numPages = Math.ceil(numRows / numPerPage);
        var $pager = $('<div class="pager"></div>');
        for (var page = 0; page < numPages; page++) {
            $('<span class="page-number"></span>').text(page + 1).bind('click', {
                newPage: page
            }, function(event) {
                currentPage = event.data['newPage'];
                $table.trigger('repaginate');
                $(this).addClass('active').siblings().removeClass('active');
            }).appendTo($pager).addClass('clickable');
        }
        $pager.insertAfter($table).find('span.page-number:first').addClass('active');
    });
    jQuery.fn.templateMoMenuHide = function(){
        return this.each(function(){
            $(this)
                .removeClass("shadow-top-down")
                .animate({opacity: 0,top: 120}, 240,"easeOutSine",function(){
                    $(this).hide();
                });
            return true;
        });
    }
    // Template Mo menu show
    jQuery.fn.templateMoMenuShow = function(){
        return this.each(function(){
            $(this)
                .addClass("shadow-top-down")
                .show()
                .css({opacity: 0,top: 120})
                .animate({opacity: 1,top: 130}, 40,"easeInSine");
            return true;
        });
    }
    // Menu click on plus btn
    $('.show-menu a').on('click', function(e){
        // When nav is visible make nav hide
        if($('nav').is(":visible")){
            $('nav:visible').templateMoMenuHide();
        // When nav is not visible make nav show
        }else{
            $('nav').templateMoMenuShow();
        }
        return false;
    });
    // Menu hide when click on any area of document
    $(document).on('click', function(e){
        $('nav:visible').templateMoMenuHide();
        return true;
    });
    // Chrome need different css style sheet for smooth scrolling.
    if($.templatemo_is_chrome){
        $("html").attr("style","overflow:auto;");
        $("body").attr("style","overflow:auto;height:auto;");
    }
    // Menu scroll to.
    $('a.scroll_effect').on('click', function(e){
        target_element = $(this).attr('href');
        scroll_to = $(target_element).offset().top;
        if($(window).scrollTop() != scroll_to && target_element !== undefined){
            // Chrome scroll to calculation and other browser scroll to calculation is different.
            if($.templatemo_is_chrome){
                body_scroll_target = scroll_to;
            }else{
                body_scroll_target = $("body").scrollTop()+scroll_to;
            }
            $('html,body').animate({scrollTop:body_scroll_target},1000);
        }
        // If menu is visible hide the nav.
        $('nav:visible').templateMoMenuHide();
        return false;
    });
});