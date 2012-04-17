(function ($) {
    
    $.fn.djCrop = function (options) {
        
        var id = '#' + $(this).attr('id');
	    	
        function updateCoords(object, c){
			$(id + '_1').attr('value', c.x);
			$(id + '_2').attr('value', c.y);
			$(id + '_3').attr('value', c.w);
			$(id + '_4').attr('value', c.h);
		}
		
		var jcrop_api;
		
		$(id + '_0').click(function(){
			if (jcrop_api){
				jcrop_api.destroy();				
			}
			$('#tempImage').remove();
			$('.aspect').remove();
			$(this).fileupload({
		        dataType: 'json',
		        url: UPLOAD_PATH,
		        done: function (e, data) {
		            $.each(data.result, function (index, file) {
		                imagePath = file.url;
		                var tempImageContainer = $('<div>');
						var tempImage = $('<img>');
						tempImage.attr('src', imagePath);
						tempImage.attr('id', 'tempImage');
						tempImageContainer.append(tempImage);
						$(id).append(tempImageContainer);
						$('#tempImage').Jcrop({			
				            onChange: function(c) { updateCoords(id + '_0', c); },
				            aspectRatio: options.ratio,
				            maxSize: [300,0]
						},function(){
							jcrop_api = this;
						});
						var aspect = $('<div><label class="aspect">Overide Aspect Ratio:</label><input class="aspect" style="width: 40px; margin-left: 10px;" type="text" id="' + id + '_aspect" /></div>');
						$(id).append(aspect);
						
						aspect.change(function(){
							jcrop_api.setOptions({ aspectRatio: $(this).val() });
						});
						
						$(id + '_5').attr('value', file.id);
		            });
		        }
		    });			
		});
        
    };

})(jQuery);

