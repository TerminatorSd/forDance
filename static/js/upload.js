//下面用于图片上传预览功能
function setImagePreview(avalue) {
　　var docObj=document.getElementById("doc");

　　var imgObjPreview=document.getElementById("preview");
　　if(docObj.files &&docObj.files[0])
　　{
　　　　//火狐下，直接设img属性
　　　　imgObjPreview.style.display = 'block';
　　　　imgObjPreview.style.width = '150px';
　　　　imgObjPreview.style.height = '180px';

　　　　//火狐7以上版本不能用上面的getAsDataURL()方式获取，需要一下方式
　　　　imgObjPreview.src = window.URL.createObjectURL(docObj.files[0]);
　　}
　　else
　　{
　　　　//IE下，使用滤镜
　　　　docObj.select();
　　　　var imgSrc = document.selection.createRange().text;
　　　　var localImagId = document.getElementById("localImag");
　　　　//必须设置初始大小
　　　　localImagId.style.width = "150px";
　　　　localImagId.style.height = "180px";
　　　　//图片异常的捕捉，防止用户修改后缀来伪造图片
　　　　try{
　　　　　　localImagId.style.filter="progid:DXImageTransform.Microsoft.AlphaImageLoader(sizingMethod=scale)";
　　　　　　localImagId.filters.item("DXImageTransform.Microsoft.AlphaImageLoader").src = imgSrc;
　　　　}
　　　　catch(e)
　　　　{
　　　　　　alert("您上传的图片格式不正确，请重新选择!");
　　　　　　return false;
　　　　}
　　　　imgObjPreview.style.display = 'none';
　　　　document.selection.empty();
　　}
　　return true;
}

function FW(event){
    alert('hah');
    var input = document.getElementById('doc');
    var reader = new FileReader();
    var csrf = document.getElementsByTagName('input')[0].value;
    console.log(csrf);
//    var dataAF = {};
//    dataAF.img = reader.result;
//        data.csrfmiddlewaretoken = csrf;
    reader.onload = function(){
        var dataAF = {};
        dataAF.img = reader.result;
        dataAF.csrfmiddlewaretoken = csrf;

        httpHelper({
            type:'post',
            async:'true',
            data:dataAF,
            url:'/upload/',
            success:function(){
                //上传成功
            },
            error:function(){
                //上传失败
            }
        });
    };
    reader.readAsBinaryString(input.files[0]);
};
function httpHelper(params) {
    var request;
    if(XMLHttpRequest)
        request=new XMLHttpRequest();
    else
        request=new ActiveXObject("Microsoft.XMLHTTP");
    request.onreadystatechange = function () {
        if (request.readyState == 4) {
            if (request.status == 200) {
                if (params.success)
                    params.success(request.responseText);
            }
            else if (parseInt(request.status / 100) == 4) {
                if (params.error)
                    params.error(request.responseText);
            }
        }
    }
    request.open(params.type, params.url, params.async);
    try {
        request.send(params.data||null);
    } catch (e) {
        if (params.error)
            params.error(request.responseText);
    }
}