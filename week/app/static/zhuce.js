$(function(){
    var yz1 = false;
    var yz2 = false;
    $("#username").blur(function () {
        check_name();
    });
    function check_name() {
        var usernameinput = $("#username");
        var username = usernameinput.val();
        var usernamere = /^[\u4E00-\u9FA5]{1,5}$|^[\u4E00-\u9FA5]{1,5}\d\d$/g;
        // console.log(username)
        if (!usernamere.test(username)) {
            usernameinput.next().remove();
            usernameinput.parent().addClass("has-error");
            // <p class="help-block">两次密码不相同！</p>
            usernameinput.parent().append("<p class=\"help-block\">用户名最长为5位汉字或者5位汉字加两位数字！</p>");
        }
        else {
            usernameinput.parent().removeClass("has-error");
            usernameinput.next().remove();
            yz1 = true;
        }
    }
    $("#passwd2").blur(function () {
        check_passwd();
    });
    function check_passwd(){
        var passwdinput = $("#passwd");
        var passwd2input = $("#passwd2");
        if (passwdinput.val() != passwd2input.val()) {
            passwdinput.next().remove();
            passwdinput.parent().addClass("has-error");
            passwd2input.parent().addClass("has-error");
            passwdinput.parent().append("<p class=\"help-block\">两次密码不相同！</p>");
        }
        else {
            passwdinput.parent().removeClass("has-error");
            passwd2input.parent().removeClass("has-error");
            passwdinput.next().remove();
            yz2 = true;
        }
    }
 // 如果表单是flask来生成的不需要再写提交方法，只需要写验证方法
    $('#submit').click(function () {
        check_name();
        check_passwd();
        if (yz1 ==false || yz2 == false){
            return false;
            }
        // var data = $(".form").serialize();
        // $.ajax({
        //     type:"POST",
        //     url:"/useradd",
        //     data: data,
        //     success : function () {
        //         // location.href="/";
        //     },
        //     error:function () {
        //         location.href="/useradd";
        //     console.log("提交失败！");
        //     }
        // });
    });
});