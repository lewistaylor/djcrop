(function ($) {
    
    $.fn.djCrop = function (options) {
        
        var id = '#' + $(this).attr('id');
	    	
        function updateCoords(object, c){
			$(id + '_1').attr('value', c.x);
			$(id + '_2').attr('value', c.y);
			$(id + '_3').attr('value', c.w);
			$(id + '_4').attr('value', c.h);
		}
		
		$(id + '_0').click(function(){
			$(this).fileupload({
		        dataType: 'json',
		        url: UPLOAD_PATH,
		        done: function (e, data) {
		            $.each(data.result, function (index, file) {
		                imagePath = file.url;
						var tempImage = $('<img>');
						tempImage.attr('src', imagePath);
						tempImage.attr('id', 'tempImage');
						$(id).append(tempImage);
						$('#tempImage').Jcrop({			
				            onChange: function(c) { updateCoords(id + '_0', c); }
						});
						$(id + '_5').attr('value', file.id);
		            });
		        }
		    });			
		});
        
    };

})(jQuery);

