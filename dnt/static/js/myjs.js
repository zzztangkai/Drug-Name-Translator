

$(document).ready(function(){
    $("#btnfile").click(function(){
        $("#id_file").click();
    });

    //SCRIPT TO OPEN THE CROP WINDOW WITH THE PREVIEW
      $("#id_file").change(function (){
          var reader = new FileReader();
          reader.onload = function(e){
            $("#image").attr("src", e.target.result);
            $("#cropDiv").modal("show");
          }
          reader.readAsDataURL(this.files[0]);
      });

      //SCRIPTS TO HANDLE THE CROPPER BOX
      var $image = $("#image");
      var cropBoxData;
      var canvasData;
      $("#cropDiv").on("shown.bs.modal", function () {
        $image.cropper({
          viewMode: 1,
          minCropBoxWidth: 10,
          minCropBoxHeight: 10,
          ready: function () {
            $image.cropper("setCanvasData", canvasData);
            $image.cropper("setCropBoxData", cropBoxData);
          }
        });
      }).on("hidden.bs.modal", function () {
        cropBoxData = $image.cropper("getCropBoxData");
        canvasData = $image.cropper("getCanvasData");
        $image.cropper("destroy");
      });

      //SCRIPT TO COLLECT THE DATA AND POST TO THE SERVER
      $(".js-crop-and-upload").click(function () {
        var cropData = $image.cropper("getData");
        $("#id_x").val(cropData["x"]);
        $("#id_y").val(cropData["y"]);
        $("#id_height").val(cropData["height"]);
        $("#id_width").val(cropData["width"]);
        $("#formUpload").submit();
      });

      //SCRIPT TO TO DRAG THE CROP WINDOW
      $("#cropDiv").draggable({
        drag: function (event, ui) {
          ui.position.top += (ui.offset.top - ui.originalPosition.top) * 0.03;
          ui.position.left += (ui.offset.left - ui.originalPosition.left) * 1.2;
        },
        start: function(event, ui){
          $("#cropDivHeader").css('opacity', '0.75');
        },
        stop: function(event, ui){
          $("#cropDivHeader").css('opacity', '1.0');
        }
      });
  });
