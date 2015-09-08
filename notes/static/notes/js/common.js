/**
 * Created by Jeezy on 07.09.2015.
 */

  $(document).ready(function () {
        $('.notes').mouseenter(function () {
            $(this).removeClass('animated bounceInDown').addClass('animated pulse');
            $(this).click(function () {
                $(this).removeClass('animated pulse').addClass('animated flip');
            });
        }).mouseleave(function () {
            $(this).removeClass('animated pulse')
        });

        $('.notes_labels').mouseenter(function () {
            $(this).css("overflow", "visible");
        }).mouseleave(function () {
            $(this).css("overflow", "hidden");
        });

        $('.labels_in_show').click(function () {
            var hidden = $(this).addClass('animated zoomOutUp');
            setTimeout(function () {
                hidden.addClass('hidden');
            }, 1000);
        });

        $('.messenger').delay(2000).slideUp();
    });